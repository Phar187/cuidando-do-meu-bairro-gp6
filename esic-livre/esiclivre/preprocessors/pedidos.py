# coding: utf-8

import collections
import os
import string
import time

import arrow
import bs4
import dateutil.parser
from flask import current_app
import internetarchive
from internetarchive import get_session
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound

from cuidando_utils import db

from esiclivre import models

VALID_ATTACHMENTS_NAME_CHARS = string.ascii_lowercase + string.digits + '.-_'


def parse_date(text):
    return arrow.get(dateutil.parser.parse(text, dayfirst=True))


class ParsedPedido(object):

    def __init__(self, raw_data, browser):

        self._browser = browser
        self._raw_data = raw_data
        self._main_data = self._get_main_data()

        if self._main_data:
            self._details = self._get_details()
            self.attachments = self._get_attachments()
            self.situation = self._get_situation()
            self.request_date = self._get_request_date()
            self.history = self._get_history()
            # TODO: criar a função que pega o deadline, ver em browser.py como fazer já que lá isso está implementado. Parece usar 2 jeitos diferentes.
            # self.deadline = self._get_deadline()

    def _get_main_data(self):
        return self._raw_data.form

    def _get_details(self):
        return self._main_data.select('#ctl00_MainContent_dtv_pedido')[0]

    @property
    def protocol(self):
        data = self._details.tbody.select('tr')[0]
        _, protocol = data.select('td')
        return int(protocol.text.strip())

    @property
    def interessado(self):
        data = self._details.tbody.select('tr')[1]
        _, interessado = data.select('td')
        return interessado.text.strip()

    def _get_request_date(self):
        data = self._details.tbody.select('tr')[2]
        _, opened_at = data.select('td')
        # return dateutil.parser.parse(opened_at.text.strip(), dayfirst=True)
        return parse_date(opened_at.text.strip())

    @property
    def orgao(self):
        data = self._details.tbody.select('tr')[3]
        _, orgao = data.select('td')
        return orgao.text.strip()

    @property
    def contact_option(self):
        data = self._details.tbody.select('tr')[4]
        _, option = data.select('td')
        return option.text.strip()

    @property
    def description(self):
        data = self._details.tbody.select('tr')[5]
        _, desc = data.select('td')
        return desc.text.strip()

    @property
    def allow_recurso(self):
        '''Return True if recurso is allowed.'''
        for id_ in [
            'ctl00_MainContent_btnAbrirRecurso',
            'ctl00_MainContent_btnSolicitarEsclarecimento'
        ]:
            if self._raw_data.select(f'#{id_}'):
                return True
        return False

    def _get_attachments(self):
        grid = self._main_data.select('#ctl00_MainContent_grid_anexos_resposta')

        if not grid:
            return ()  # 'Sem anexos.'
        else:
            grid = grid[0]

        data = grid.tbody.select('tr')[1:]
        if not data or not any([i.text.split() for i in data]):
            return ()  # 'Sem anexos.'

        result = ()
        for item in data:

            filename, created_at, fileid = item.select('td')

            attachment = collections.namedtuple(
                'PedidoAttachment', ['filename', 'created_at'])
            attachment.filename = clear_attachment_name(filename.text)
            # attachment.created_at = dateutil.parser.parse(
            #     created_at.text.strip(), dayfirst=True)
            attachment.created_at = parse_date(created_at.text.strip())

            # upload_attachment_to_internet_archive(
            #     self.protocol, attachment.filename
            # )

            print("anexo")
            print(attachment.filename)
            result += (attachment,)
        return result

    def _get_situation(self):
        fieldset = self._main_data.select('#fildSetSituacao')[0]
        data = fieldset.tbody.select('tr')[0]
        _, situation = data.select('td')[:2]
        return situation.text.strip()

    def _get_history(self):

        grid = self._main_data.select('#ctl00_MainContent_grid_historico')[0]

        # get the 2th to skip header...
        data = grid.tbody.select('tr')[1:]

        result = ()
        for item in data:
            situation, justification, responsible = item.select('td')[1:]
            date = item.span

            history = collections.namedtuple(
                'PedidoHistory',
                ['situation', 'justification', 'responsible', 'date']
            )
            history.situation = situation.text.strip()
            history.justification = justification.text.strip()
            history.responsible = responsible.text.strip()
            history.date = parse_date(date.text.strip())

            result += (history,)

        try:
            result = sorted(result, key=lambda h: h.date)
        except:
            pass

        return result

    def upload_modified_attachments(self):

        attachments_el_id = 'ctl00_MainContent_grid_anexos_resposta'
        # If pedido has no attachments
        if not self._raw_data.select('#' + attachments_el_id):  # noqa
            return None

        # Get the current pedido and its attachments from the DB
        db_pedido = (
            db.session.query(models.Pedido)
            .filter_by(protocol=self.protocol)
            .options(joinedload('attachments'))
            .one())
        db_attachments = db_pedido.attachments if db_pedido else []

        for attachment in self.attachments:
            # Get last created_at time saved in DB
            old_created_at = next(
                (a.created_at
                 for a in db_attachments
                 if a.name == attachment.filename),
                None
            )
            # old_created_at = [a.created_at for a in db_attachments
            #                   if a.name == attachment.filename]
            # old_created_at = old_created_at[0] if old_created_at else None

            # Download and upload attachments that created_at changed
            if not old_created_at or (attachment.created_at != old_created_at):
                print(
                    'Anexo modificado ou novo. Baixando e enviando para IA.')

                attachments_el = self._browser.navegador.find_element_by_id(
                    attachments_el_id)
                if attachments_el:
                    # TODO: atualmente está baixando TODOS os anexos do pedido,
                    # o certo seria baixar apenas o anexo cuja data realmente
                    # mudou
                    self.download_pedido_attachments(attachments_el)

                upload_attachment_to_internet_archive(
                    self.protocol, attachment.filename
                )

    def download_pedido_attachments(self, attachments):

        for attachment in attachments.find_elements_by_tag_name('input'):

            # baixar o arquivo
            attachment.click()

            # a ideia aqui é que se houver algum arquivo .part, ou seja, algum
            # download ainda não terminou, o processo aguarde até esses
            # arquivos serem baixados ou completar N tentativas

            max_retries = 0
            if str('.part') in os.listdir(current_app.config['DOWNLOADS_PATH']):  # noqa
                print("Existe algum download inacabado...")
                while max_retries != 10:

                    download_dir = os.listdir(
                        current_app.config['DOWNLOADS_PATH']
                    )

                    uncomplete_download = next(
                        (arq for arq in download_dir if arq.endswith('.part')),
                        None
                    )

                    if not uncomplete_download:
                        print("Sem downloads inacabados...")
                        break
                    else:
                        print("Aguardar 10 segundos...")
                        time.sleep(10)
                        max_retries += 1


class Pedidos(object):

    _parsedpedidos = []
    _pedido_pagesource = []

    def set_full_data(self, browser):
        self._full_data = browser.navegador.find_element_by_id(
            'ctl00_MainContent_grid_pedido')

    def get_all_pages_source(self, browser):

        total_of_pedidos = len(self._full_data.find_elements_by_tag_name('a'))
        print('pedidos per order in consultar_pedido page: ')
        for pos in range(total_of_pedidos):
            print(f' {pos}')

            self.set_full_data(browser)

            tries = 0
            while browser.navegador.current_url.endswith('consultar_pedido_v2.aspx'):

                if tries > 10:
                    print('Error: Couldn\'t open pedido page!')
                    raise

                # Sometimes the link get stuck. Change page to next pedido and go back.
                # Reloading the page, or changing to previous pedido don't work...
                if tries >= 1:
                    # browser.navegador.refresh()
                    self._full_data.find_elements_by_tag_name('a')[pos+tries].click()
                    time.sleep(2)
                    browser.navegador.back()
                    time.sleep(2)
                    self.set_full_data(browser)

                self._full_data.find_elements_by_tag_name('a')[pos].click()
                time.sleep(1)
                tries += 1

            pagesource = bs4.BeautifulSoup(browser.navegador.page_source, 'html5lib')

            self._pedido_pagesource.append(pagesource)
            pedido = self.process_pedidos(browser, pagesource)
            fix_attachment_name_and_extension()
            pedido.upload_modified_attachments()
            browser.navegador.back()
        fix_attachment_name_and_extension()

    def process_pedidos(self, browser, page_source=None):

        # Existe a possibilidade da pagina não retornar um codigo fonte válido
        # a classe que estrutura o pedido retornará None se o código
        # fonte não for válido...
        if page_source:
            pedido = ParsedPedido(page_source, browser)
            self._parsedpedidos.append(pedido) if pedido else None
            return pedido
        else:
            self._parsedpedidos = list(p for p in (
                ParsedPedido(pp, browser) for pp in self._pedido_pagesource
                ) if p._main_data
            )
            return self._parsedpedidos

    def get_all_parsed_pedidos(self):
        return self._parsedpedidos


def clear_attachment_name(name):

    name = name.strip().lower()

    return ''.join([l for l in name if l in VALID_ATTACHMENTS_NAME_CHARS])


def fix_attachment_name_and_extension():
    # remover caracter invalidos
    # mudar extensão para lowercase
    # apagar arquivos .part (nessa etapa, se um arquivo ainda é .part é porque
    # o download falhou).
    download_dir = current_app.config['DOWNLOADS_PATH']
    for _file in os.listdir(download_dir):
        # _file = _file.decode('utf8')
        # print("file: {}".format(_file))
        _file_fullpath = '{}/{}'.format(download_dir, _file)

        if _file.endswith('.part'):
            os.remove(_file_fullpath)
        else:
            os.rename(
                _file_fullpath,
                '{}/{}'.format(download_dir, clear_attachment_name(_file))
            )


def update_pedido_messages(scrapped_pedido, pedido):
    '''Update messages for a pedido.'''
    new_insetion = False
    for item in scrapped_pedido.history:
        # Check if is a new msg
        already_inserted = False
        for itemDB in pedido.history:
            # justification can be empty, so using all fields
            if (item.date == itemDB.date and
               item.justification == itemDB.justification and
               item.situation == itemDB.situation and
               item.responsible == itemDB.responsible):
                already_inserted = True

        # Insert if is a new msg
        if not already_inserted:
            message = models.Message(
                date=item.date,
                justification=item.justification,
                responsible=item.responsible,
                situation=item.situation,
                pedido_id=pedido.id)
            db.session.add(message)
            new_insetion = True

    db.session.commit() if new_insetion else None


def create_pedido_attachments(scrapped_pedido):

    attachments = []
    for item in scrapped_pedido.attachments:

        attachment = models.Attachment()
        attachment.created_at = item.created_at
        attachment.name = item.filename
        base_url = 'https://archive.org/download'
        attachment.ia_url = (
            u'{base}/{prefix}_pedido_{protocol}/{filename}'.format(
                base=base_url,
                prefix=current_app.config['ATTACHMENT_URL_PREFIX'],
                protocol=scrapped_pedido.protocol,
                filename=item.filename
            )
        )

        db.session.add(attachment)
        attachments.append(attachment)
    db.session.commit() if attachments else None

    return attachments


def save_pedido_into_db(scrapped_pedido):
    # check if there is a object with the same protocol
    pedido = models.Pedido.query.filter(
        models.Pedido.protocol == scrapped_pedido.protocol)
    pedido = pedido.options(joinedload('history')).first()
    if not pedido:
        # if not, create one
        default_author = current_app.config['DEFAULT_AUTHOR']
        try:
            author = db.session.query(models.Author).filter(
                models.Author.name == default_author
            ).one()
        except NoResultFound:
            author = models.Author(name=default_author)
            db.session.add(author)
            db.session.commit()

        pedido = models.Pedido(protocol=scrapped_pedido.protocol, author=author)
        pedido.add_keyword('recuperado')
        db.session.add(pedido)

    # TODO: O que fazer se o orgão não existir no DB?
    if not scrapped_pedido.orgao:
        orgao_name = 'desconhecido'
    else:
        orgao_name = scrapped_pedido.orgao

    orgao = models.Orgao.query.filter_by(name=orgao_name).first()
    if not orgao:
        orgao = models.Orgao(name=orgao_name)
        db.session.add(orgao)
        db.session.commit()
    pedido.orgao_name = orgao.name

    pedido.interessado = scrapped_pedido.interessado
    pedido.situation = scrapped_pedido.situation
    pedido.request_date = scrapped_pedido.request_date
    pedido.contact_option = scrapped_pedido.contact_option
    pedido.description = scrapped_pedido.description
    pedido.allow_recurso = scrapped_pedido.allow_recurso
    # TODO: usar deadline aqui
    # pedido.deadline = scrapped_pedido.deadline
    # TODO: salvar no pedido alguma informação sobre se pode fazer recurso ou não

    db.session.commit()

    update_pedido_messages(scrapped_pedido, pedido)

    if scrapped_pedido.attachments:
        pedido.attachments = create_pedido_attachments(scrapped_pedido)


def upload_attachment_to_internet_archive(pedido_protocol, filename):

    download_dir = current_app.config['DOWNLOADS_PATH']
    downloaded_attachments = os.listdir(download_dir)

    # if filename not in [a.decode('utf8') for a in downloaded_attachments]:
    if filename not in downloaded_attachments:
        print("Arquivo {!r} não existe!.".format(filename))
        # TODO: O que fazer se o arquivo não estiver disponivel?
        # Já temos um caso onde o download não completa, mas por falha no
        # servidor do esic.
        return None
    else:

        # try:
        #     # get mediatype from file extension
        #     mediatype = filename.rpartition('.')[2]
        # except:
        #     mediatype = None

        ia_session = get_session(config={'s3': {
            'access': current_app.config['IAS3_ACCESS_KEY'],
            'secret': current_app.config['IAS3_SECRET_KEY']}})
        item = ia_session.Item('{prefix}_pedido_{protocol}'.format(
            prefix=current_app.config['ATTACHMENT_URL_PREFIX'],
            protocol=pedido_protocol))
        metadata = dict(
            # mediatype=mediatype,
            created_at=arrow.now().isoformat()
        )
        result = item.upload(
            '{}/{}'.format(download_dir, filename), metadata=metadata
        )

        if not result or result[0].status_code != 200:
            # TODO: O que fazer nessa situação?
            print("Erro ao executar upload.")
        else:
            os.remove('{}/{}'.format(download_dir, filename))


def update_pedidos_list(browser):
    # garantir que a tela inicial seja a de consulta de pedidos.
    browser.ir_para_consultar_pedido()

    pedidos = Pedidos()
    pedidos.set_full_data(browser)
    # linhas = pedidos._full_data.find_elements_by_tag_name('tr')[1:]
    pedidos.get_all_pages_source(browser)
    # pedidos.process_pedidos(browser)

    for pedido in pedidos.get_all_parsed_pedidos():
        save_pedido_into_db(pedido)

    # registrar atualização do dia
    db.session.add(
        models.PedidosUpdate(date=arrow.now())
    )
    db.session.commit()

    print("Pedidos atualizados. Atualização registrada.")
