#!/usr/bin/env python
# coding: utf-8

import os
# import requests
# import shutil
import random
import time
import pickle
# from multiprocessing import Process, Manager

import arrow
from flask import current_app
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import TimeoutException

from cuidando_utils import db

from .models import Orgao, UserMessage, PedidosUpdate, OrgaosUpdate
from .preprocessors import pedidos as pedidos_preproc
# from .sender import subscribe_user_to_notifications


class LoginNeeded(Exception):
    pass


class ESicLivre(object):

    _last_update_of_orgao_list = None

    def __init__(self, firefox, email, senha, pasta):
        '''"firefox" é o caminho para o binário do Firefox a ser usado.
        'pasta' é o caminho para a pasta onde salvar os downloads.'''
        self.firefox = firefox
        self.pasta = pasta
        self.email = email
        self.senha = senha
        # self.app = app

        self.navegador = None
        # self.logger = None

        # manager = Manager()
        # TODO: não tem problema essa troca? então reestruturar tudo abaixo
        # self.safe_dict = manager.dict()
        # self.safe_dict = {}
        # self.clear_captcha()
        # self.stop()

        # self.try_break_audio_captcha = True
        self.nome_audio_captcha = 'somCaptcha.wav'
        self.recognizer = sr.Recognizer()

        self.user_agent = (
            'Mozilla/5.0 (X11; Linux x86_64; rv:28.0)'
            ' Gecko/20150101  Firefox/45.0'
        )
        self.base_url = 'http://esic.prefeitura.sp.gov.br'
        self.login_url = self.base_url + '/Account/Login.aspx'

        self.logado = False
        self.ja_tentou_cookies_salvos = False
        # self.rodar_apenas_uma_vez = False

    # def config(self, **kwargs):
    #     for k, v in kwargs.items():
    #         setattr(self, k, v)

    def salvar_cookies(self):
        '''Salva os cookies atuais do navegador.'''
        pickle.dump(self.navegador.get_cookies(), open('cookies.pkl', 'wb'))

    def carregar_cookies(self):
        '''Carrega os cookies do navegador salvos anteriormente.'''
        try:
            cookies = pickle.load(open('cookies.pkl', 'rb'))
        except IOError:
            print('! Couldn\' load cookies.')
            return False
        for cookie in cookies:
            self.navegador.add_cookie(cookie)
        return True

    def esta_em_login(self):
        '''Verifica se está na página de login.'''
        return self.navegador.current_url == self.login_url

    def criar_navegador(self):
        '''Retorna um navegador firefox configurado para salvar arquivos
        baixados em 'pasta'.'''
        print('Configuring and initiating browser...')
        fp = webdriver.FirefoxProfile()
        fp.set_preference('browser.download.folderList', 2)
        fp.set_preference('browser.download.manager.showWhenStarting', False)
        fp.set_preference('browser.download.dir', self.pasta)
        tipos = ','.join([
            'text/csv', 'audio/wav', 'audio/x-wav',
            'image/jpeg', 'application/octet-stream'])
        fp.set_preference('browser.helperApps.neverAsk.saveToDisk', tipos)
        fp.set_preference('general.useragent.override', self.user_agent)
        # O binário do navegador deve estar na pasta firefox
        binary = FirefoxBinary(self.firefox)
        self.navegador = webdriver.Firefox(
            firefox_binary=binary, firefox_profile=fp
        )
        self.navegador.implicitly_wait(20)

    def ir_para_registrar_pedido(self):
        self.navegador.get(self.base_url + '/registrar_pedido_v2.aspx')

    def ir_para_consultar_pedido(self):
        self.navegador.get(self.base_url + '/consultar_pedido_v2.aspx')

    def ir_para_login(self):
        self.navegador.get(self.login_url)

    def try_to_transcribe_audio_captcha(self):
        print('Transcribing audio captcha...')
        audio_path = os.path.join(self.pasta, self.nome_audio_captcha)
        with sr.WavFile(str(audio_path)) as source:
            audio = self.recognizer.record(source)
        try:
            return self.recognizer.recognize_google(audio, language=str('pt-BR'))
        except LookupError:
            return None

    def baixar_audio_captcha(self):
        # Removes the last downloaded audio file, avoiding adding (1) to
        # the end of the file name
        cam_audio = os.path.join(self.pasta, self.nome_audio_captcha)
        try:
            os.remove(cam_audio)
        except (OSError, IOError):
            pass
        print('Downloading audio captcha...')
        # Esse número deve ser usado para evitar problemas com a cache
        n = random.randint(1, 400)
        link = self.base_url + '/Account/pgAudio.ashx?%s' % n

        self.navegador.set_page_load_timeout(1)
        try:
            self.navegador.get(link)
        except TimeoutException:
            pass
        self.navegador.set_page_load_timeout(10)

        time.sleep(3)
        while str(self.nome_audio_captcha + '.part') in os.listdir(self.pasta):
            print('Waiting download finish...')
            time.sleep(1)
        print('Downloaded.')

    # def baixar_imagem_captcha(self):
    #     # Removes the last downloaded audio file, avoiding adding (1) to
    #     # the end of the file name
    #     cam_imagem = os.path.join(self.pasta, self.nome_audio_captcha)
    #     try:
    #         os.remove(cam_imagem)
    #     except (OSError, IOError):
    #         pass
    #     link = self.base_url + '/Account/pgImagem.ashx'

    #     nome = 'ASP.NET_SessionId'
    #     cookie = self.navegador.get_cookie(nome)
    #     headers = {
    #         'User-Agent': self.user_agent,
    #     }
    #     if cookie and cookie.get('value', False):
    #         headers.update({'Cookie': '{0}={1}'.format(nome, cookie['value'])})

    #     r = requests.get(link, stream=True, headers=headers)
    #     r.raw.decode_content = True
    #     import tempfile
    #     with tempfile.NamedTemporaryFile() as out_file:
    #         shutil.copyfileobj(r.raw, out_file)

    def gerar_novo_captcha(self):
        self.navegador.find_element_by_id(
            'ctl00_MainContent_btnAtualiza').click()

    def clicar_login_entrar(self):
        self.navegador.find_element_by_id('ctl00_MainContent_btnEnviar').click()

    def clicar_recorrer(self):
        self.navegador.find_element_by_id(
            'ctl00_MainContent_btnSolicitarEsclarecimento').click()

    def entrar_dados_login(self, captcha):
        params = {
            'ctl00_MainContent_txt_email': self.email,
            'ctl00_MainContent_txt_senha': self.senha,
            'ctl00_MainContent_txtValorCaptcha': captcha,
        }
        for k, v in params.items():
            element = self.navegador.find_element_by_id(k)
            element.clear()
            element.send_keys(v)

    def entrar_no_sistema(self, captcha):
        if not self.esta_em_login():
            self.ir_para_login()
        self.entrar_dados_login(captcha)
        self.clicar_login_entrar()

    # def preparar_receber_captcha(self):
    #     self.ir_para_login()
    #     self.baixar_imagem_captcha()
    #     self.clear_captcha()

    def criar_dicio_orgaos(self):
        '''Cria o dicionário com os órgãos e botões para selecioná-los.
        Precisa estar na página de 'Registrar Pedido'.'''
        # Pega todos os elementos 'options' dentro do seletor
        select = self.navegador.find_element_by_id(
            'ctl00_MainContent_ddl_orgao')
        options = select.find_elements_by_tag_name('option')
        # Cria dicionário (nome do órgão: elemento da interface que pode ser
        # clicado para selecioná-lo). Exclui o primeiro item que é 'Selecione'.
        return dict([(i.text, i) for i in options[1:]])

    def entrar_com_texto_pedido(self, texto):
        textarea = self.navegador.find_element_by_id(
            'ctl00_MainContent_txt_descricao_solicitacao')
        textarea.clear()
        textarea.send_keys(texto)
        # Autorizar divulgação da pergunta
        self.navegador.find_element_by_id('ctl00_MainContent_rbdSim').click()

    def clicar_enviar_pedido(self):
        '''Enviar pedido de informação'''
        self.navegador.find_element_by_id(
            'ctl00_MainContent_btnEnviarAntes').click()

    def check_login_needed(self):
        if self.esta_em_login():
            raise LoginNeeded

    # Funções Gerais

    def postar_pedido(self, orgao, texto):
        print('> going to new pedido page')
        self.ir_para_registrar_pedido()
        self.check_login_needed()
        # TODO: testar se está na página de fazer pedido
        print('> getting orgaos buttons')
        orgaos = self.criar_dicio_orgaos()
        # TODO: testar se órgão existe
        print('> selecting orgao')
        orgaos[orgao].click()
        print('> pedido text to input')
        self.entrar_com_texto_pedido(texto)
        print('> sending...')
        self.clicar_enviar_pedido()

        print('> getting protocolo')
        # Returns protocolo
        protocolo = self.navegador.find_element_by_id(
            'ctl00_MainContent_lbl_protocolo_confirmar'
        ).text
        deadline = self.navegador.find_element_by_id(
            'ctl00_MainContent_lbl_prazo_atendimento_confirmar'
        ).text
        return int(protocolo), arrow.get(deadline, ['DD/MM/YYYY'])

    def postar_recurso(self, protocolo, texto):
        print('> estou indo para a página para consultar pedidos')
        self.ir_para_consultar_pedido()
        self.check_login_needed()

        print('> estou indo para a pagina do pedido')
        self.navegador.find_element_by_xpath(
            "//table//tr[td[text()='" + protocolo + "']]//a"
        ).click()

        try:
            print("> estou tentando ir para pagina de recurso de segunda instancia")
            self.navegador.find_element_by_id(
                "ctl00_MainContent_btnAbrirRecurso"
            ).click()

            select = Select(self.navegador.find_element_by_tag_name("select"))
            select.select_by_value("13")
        except Exception as e:
            print(e)
            print("> estou indo para a pagina do para abrir recurso")
            self.navegador.find_element_by_id(
                "ctl00_MainContent_btnSolicitarEsclarecimento"
            ).click()

        deadline = self.navegador.find_element_by_xpath(
            "//tr[td/b/text()='Prazo de resposta:']//input"
        ).get_attribute("value")

        self.navegador.find_element_by_tag_name("textarea").send_keys(texto)

        try:
            self.navegador.find_element_by_id(
                "ctl00_MainContent_btnEnviar"
            ).click()
        except Exception as e:
            print(e)
            self.navegador.find_element_by_id(
                "ctl00_MainContent_btnEnviarRecurso"
            ).click()

        return arrow.get(deadline, ['DD/MM/YYYY'])

    def lista_de_orgaos(self):
        self.ir_para_registrar_pedido()
        # TODO: ver se realmente está na página
        return self.criar_dicio_orgaos().keys()

    def set_captcha(self, value):
        self.safe_dict['captcha'] = value

    # def get_captcha(self):
    #     return self.safe_dict['captcha']

    # def clear_captcha(self):
    #     self.safe_dict['captcha'] = ''

    # def stop(self):
    #     process = Process(target=self.__stop_func__)
    #     process.start()

    # def start(self):
    #     process = Process(target=self.__run__)
    #     process.start()

    # def rodar_uma_vez(self):
    #     self.rodar_apenas_uma_vez = True
    #     self.__run__()

    def transcribe_captcha(self):
        if not self.esta_em_login():
            self.ir_para_login()
        f = True
        while f:
            self.baixar_audio_captcha()
            captcha = self.try_to_transcribe_audio_captcha()
            if captcha:
                captcha = captcha.replace('ver ', 'v')
                captcha = captcha.replace(' ', '')
                print('Transcribed captcha: %s' % captcha)
                if len(captcha) == 4:
                    # Transcrição do captcha possivelmente válida, vamos tentar logar
                    break
            # Transcrição certamente válida, pedir outro captcha
            self.gerar_novo_captcha()
        return captcha

    def run(self, force_update):
        # if not self.safe_dict.get('running'):
        # Get context needed for DB
        with current_app.app_context():
            # Set flag that can be used later to stop running
            # self.safe_dict['running'] = True
            self.criar_navegador()

            try:
                # self.preparar_receber_captcha()
                # Main loop
                # while self.safe_dict['running']:
                #     self.main_loop()

                # if not self.ja_tentou_cookies_salvos:
                #     self.login_com_cookies_salvos()
                #     self.ja_tentou_cookies_salvos = True

                if not self.logado:
                    self.login_com_captcha()

                if self.logado:
                    try:
                        self.verificar_lista_orgaos()

                        self.post_user_messages()

                        self.update_pedidos_data(force_update)

                    except LoginNeeded:
                        print('Seems to have been logged out...')

                    # print('Need new captcha...')
                    # self.preparar_receber_captcha()
            except Exception as e:
                print(e)
            finally:
                self.navegador.quit()

    def update_pedidos_data(self, force_update=False):
        '''Scrape pedidos data.'''
        last_update = db.session.query(PedidosUpdate).order_by(
            PedidosUpdate.date.desc()).first()

        if (force_update or
           (last_update and last_update.date.date() != arrow.now().date())):
            print('Atualizando dados sobre pedidos...')
            pedidos_preproc.update_pedidos_list(self)
            return True
        else:
            print('Pedidos já foram scrapeados hoje.')
            return False

    def verificar_lista_orgaos(self):
        last_update = db.session.query(OrgaosUpdate).order_by(
            OrgaosUpdate.date.desc()).first()

        if last_update and last_update.date.date() == arrow.now().date():
            print('Lista de orgaos já foi atualizada hoje.')
            return None
        else:
            print('Atualizando lista de orgaos...')
            self.update_orgaos_list()
            db.session.add(OrgaosUpdate(date=arrow.now()))
            db.session.commit()

    def login_com_cookies_salvos(self):
        '''Tenta usar cookies salvos para logar'''
        self.ir_para_consultar_pedido()
        self.carregar_cookies()
        self.ir_para_consultar_pedido()
        if not self.esta_em_login():
            self.logado = True
            print('Old cookies seems to work!')
        else:
            print('Old cookies failed...')

    def login_com_captcha(self):
        '''Tenta interagir com captcha'''
        tentativas = 0
        while not self.logado and tentativas < 50:
            tentativas += 1
            # if self.try_break_audio_captcha:
            captcha = self.transcribe_captcha()
            # else:
            #     captcha = self.get_captcha()
            print('Current captcha: %s' % captcha)

            # If captcha is unset, may need to wait someone to set it
            # If is set, login
            # if captcha:
            print('Trying to login...')
            try:
                self.entrar_no_sistema(captcha)
                if not self.esta_em_login():
                    self.logado = True
                    # self.salvar_cookies()
                    print('Seems to have logged in!')
            except Exception as e:
                print(e)

    def post_user_messages(self):
        '''Post pedidos and recursos.'''

        pending_user_messages = (
            db.session.query(UserMessage)
            .options(db.joinedload(UserMessage.pedido))
            .filter_by(state=UserMessage.states.waiting)
            .all())

        print(f'Postando {len(pending_user_messages)} pedidos/recurso...')

        for user_message in pending_user_messages:
            # Is a new Pedido
            if user_message.type == UserMessage.types.pergunta:
                protocolo, deadline = self.postar_pedido(
                    user_message.orgao_name, user_message.text
                )
                # TODO: essa primeira parte do if é só transitória
                # if not user_message.pedido:
                #     user_message.create_pedido(protocolo, deadline)
                # else:
                pedido = user_message.pedido
                pedido.protocol = protocolo
                pedido.deadline = deadline
                now = arrow.utcnow()
                pedido.request_date = now
                user_message.updated_at = now
                user_message.state = UserMessage.states.processed
                # user_message.create_pedido(protocolo, deadline)
                db.session.commit()
                print('Pedido sent.')
                # subscribe_user_to_notifications(
                #     pedido.author, pedido.get_notification_id())
                # print('User subscribed for pedido notifications.')
            # Is a Recurso to a current Pedido
            elif user_message.type == UserMessage.types.recurso:
                pedido = user_message.pedido
                protocolo = pedido.protocol
                deadline = self.postar_recurso(
                    protocolo, user_message.text
                )
                # TODO: falta colocar o deadline no Pedido
                pedido.deadline = deadline
                db.session.commit()
                print('Recurso sent!')

    def update_orgaos_list(self):
        db.session.query(Orgao).delete()
        db.session.commit()

        new_orgaos = False
        for org in self.lista_de_orgaos():
            if not Orgao.query.filter_by(name=org).first():
                db.session.add(Orgao(name=org))
                new_orgaos = True

        if new_orgaos:
            db.session.commit()
            self._last_update_of_orgao_list = arrow.utcnow()
            print(f'Last update of the orgaos list: {self._last_update_of_orgao_list}')
