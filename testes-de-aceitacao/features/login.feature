# language: pt
Funcionalidade: Login de Usuário

Contexto:
  Dado que estou na página inicial
  Quando eu clico no link "Entrar" no menu
  E o formulário de login aparece

# Cenário 1: Usuário tenta fazer login com credenciais válidas
Cenário: Login com conta válida
  E eu preencho o nome de usuário "Anamara" e a senha "123456@@"
  E eu clico no botão "Entrar"
  Então eu devo ver o perfil do usuário "Anamara"

# Cenário 2: Usuário tenta fazer login com conta inexistente
Cenário: Login com conta inexistente
  E eu preencho o nome de usuário "Perereria" e a senha "senha_teste"
  E eu clico no botão "Entrar"
  Então eu devo ver a mensagem de nome de usuário inválido "O nome de usuário parece não registrado..."

# Cenário 3: Usuário tenta fazer login com senha inválida
Cenário: Login com senha inválida
  E eu preencho o nome de usuário "Anamara" e a senha "senha_incorreta"
  E eu clico no botão "Entrar"
  Então eu devo ver a mensagem de senha inválida "Senha incorreta. Tente novamente."

# Cenário 4: Usuário recorrer a recuperar senha com email correto
Cenário: Recuperação de senha com email correto
  Quando eu clico na opção "esqueceu a senha?"
  Então eu devo ver um campo para inserir meu email
  E eu preencho o nome de usuário "papabem" e o email "pauloalves@usp.br"
  Quando eu clico no botão "Solicitar código"
  Então eu não devo ver uma mensagem de erro

# Cenário 5: Usuário recorrer a recuperar senha com email incorreto
Cenário: Recuperação de senha com email incorreto
  Quando eu clico na opção "esqueceu a senha?"
  Então eu devo ver um campo para inserir meu email
  Quando eu preencho o nome de usuário "papabem" e o email "email_incorreto@exemplo.com"
  Quando eu clico no botão "Solicitar código"
  Então eu devo ver a mensagem de erro "E-mail errado."

# Cenário 6: Logout do usuário logado
Cenário: Logout do usuário logado
  Quando eu preencho o nome de usuário "Anamaro" e a senha "123456@@"
  E eu clico no botão "Entrar"
  Então eu devo ver o nome do usuário "Anamaro" na barra de navegação
  Quando eu clico no botão com o nome de usuário "Anamaro"
  E eu devo ver as opções "Perfil" e "Sair"
  Quando eu clico no link "Sair"
  Então eu não devo ver o perfil do usuário "Anamaro"