# language: pt
Funcionalidade: Visualizar e acompanhar atividades recentes na página inicial
  Como usuário do sistema
  Quero visualizar uma lista de atividades recentes na página inicial
  E acompanhar despesas específicas para monitoramento


Contexto:
  Dado que estou na página inicial
  Quando eu clico no link "Entrar" no menu
  E o formulário de login aparece
  E eu preencho o nome de usuário "Anamara" e a senha "123456@@"
  E eu clico no botão "Entrar"
  Então eu devo ver o perfil do usuário "Anamara"


# Cenário 1
Cenário: Visualizar lista de atividades recentes na página inicial
  Quando procuro pelas atividades recentes do site
  Então devo ver uma lista de atividades recentes com detalhes como data, título e status atual


# Cenário 2
Cenário: Ver detalhes de uma atividade recente ao clicar em "Saiba mais"
  Quando clico no botão "Saiba mais" de uma atividade específica
  Então devo ser redirecionado para a página de detalhes da atividade
  E devo ver informações detalhadas sobre a atividade selecionada


# Cenário 3
Cenário: Acompanhar despesas específicas para monitoramento
  Dado que estou na página sobre detalhes da atividade recente escolhida
  E vejo o botão "Acompanhar despesa"
  Quando clico no botão "Acompanhar despesa"
  Então devo ver o botão "Deixar de acompanhar despesa"

# Cenário 4
Cenário: Procurar informações da despesa em formato JSON
  Dado que estou na página sobre uma despesa específica
  E vejo o botão "Mais informações"
  Quando clico no botão "Mais informações"
  Então devo ver as informações da despesa em formato JSON
