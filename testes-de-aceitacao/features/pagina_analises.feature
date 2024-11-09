# language: pt
Funcionalidade: Seleção de modo de visualização do gráfico de perguntas ao longo do tempo

Contexto:
    Dado que estou na página inicial
    Quando eu clico no botão para ir para a página "Análises"

    # Cenário 1: quero visualizar quantas perguntas foram feitas em cada ano
    Cenário: Organização de perguntas por ano
    E o botão ano está desabilitado pois já foi selecionado
    Então o gráfico deve estar organizado por ano

    # Cenário 2: quero visualizar quantas perguntas foram feitas em cada mês
    Cenário: Organização de perguntas por mês
    E eu clico no botão marcado como mês
    E o botão mês está desabilitado pois já foi selecionado
    Então o gráfico deve estar organizado por mês

    # Cenário 3: quero visualizar quantas perguntas foram feitas em cada dia
    Cenário: Organização de perguntas por dia
    E eu clico no botão marcado como dia
    E o botão dia está desabilitado pois já foi selecionado
    Então o gráfico deve estar organizado por dia

    # Cenário 4: que o botão ano, desabilitado quando carrega a página, é habilitado quando aperta outro botão
    Cenário: Verificar se é possível de clicar no botão ano após clicar em outro botão
    E o botão ano está desabilitado pois já foi selecionado
    E eu clico no botão marcado como mês
    E o botão mês está desabilitado pois já foi selecionado
    E o botão ano está habilitado
    E eu clico no botão marcado como ano
    E o botão ano está desabilitado pois já foi selecionado
    Então o gráfico deve estar organizado por ano