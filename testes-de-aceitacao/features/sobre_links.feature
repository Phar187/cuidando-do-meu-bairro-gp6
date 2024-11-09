# language: pt
Funcionalidade: Teste dos links da página Sobre

Contexto:
    Dado que estou na página inicial
    Quando eu clico no botão para ir para a página "Sobre"

    #Cenário 1: Clico no link para visualizar a página do colaborador Andrés
    Cenário: clico no link do Andrés
    E clico no link Andrés M. R. Martano
    Então deve abrir a página pessoal do colaborador Andrés M. R. Martano

    #Cenário 2: Clico no link para visualizar a página da colaboradora Vanessa
    Cenário: clico no link da Vanessa
    E clico no link Vanessa Alves do Nascimento
    Então deve abrir a página pessoal da colaboradora Vanessa Alves do Nascimento

    

    #Cenário 3: Clico no link para visualizar a página do repositório do projeto no Gitlab
    Cenário: clico no link do Gitlab
    E clico no link Gitlab
    Então deve abrir a página com o repositório do projeto no Gitlab

    #Cenário 6: Clico no link com o e-mail para entrar em contato com a equipe do projeto 