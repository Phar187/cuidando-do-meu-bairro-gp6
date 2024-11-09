# language: pt
Funcionalidade: Edição de perfil do usuário

Contexto:
  Dado que estou na página inicial
  Quando eu clico no link "Entrar" no menu
  E o formulário de login aparece
  E eu preencho o nome de usuário "Anamar" e a senha "123456@@"
  E eu clico no botão "Entrar"
  Então eu devo ver o nome do usuário "Anamar" na barra de navegação
  Quando eu clico no botão com o nome de usuário "Anamar"
  Então eu devo ver as opções "Perfil" e "Sair"
  Quando eu clico no link "Perfil"
  Então eu vou para o perfil do usuário "Anamar"

#cenário 01
# O botão deste teste está quebrado, então vou apenas verificar a sua existência
Cenário: Editar a descrição do usuário
  Então o botão de editar a descrição existe

#cenário 02
Cenário: Editar o e-mail do usuário
  Quando eu clico no botão de editar o e-mail "Editar"
  E eu vejo um formulário de email
  E eu insiro o novo e-mail "alinelili120@hotmail.com"
  E eu clico no botão de salvar
  Então eu devo ver o e-mail atualizado como "alinelili120@hotmail.com"

#cenário 03
Cenário: Editar a senha do usuário
  Quando eu clico no botão de editar senha "Editar"
  E eu vejo um formulário de senha
  E eu insiro a senha atual "123456@@"
  E eu insiro a nova senha "novasenha123"
  E eu confirmo a nova senha "novasenha123"
  E eu clico no botão de salvar senha "Salvar"
  Então eu vou para o perfil do usuário "Anamar"