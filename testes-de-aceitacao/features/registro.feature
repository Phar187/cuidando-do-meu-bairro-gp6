# language: pt
Funcionalidade: Registro de Usuário

Contexto:
    Dado que estou na página inicial
    Quando eu clico no link "Entrar" no menu
    E o formulário de login aparece
    Quando eu clico na opção "Crie uma conta"

  # Cenário1: Registro de Usuário com Dados Únicos
  Cenário: Usuário realiza o registro com dados únicos
    Dado que estou registrando uma conta única
    Quando eu preencho o formulário de registro com dados únicos
    E eu clico no botão "Crie uma conta"
    Então eu devo ver o perfil do usuário recém-registrado


  # Cenário 2: Registro com dados de uma conta que já existe
  Cenário: registro com dados de uma conta que já existe
    Então eu preencho o nome de usuário "Anamaro", a senha "123456@@", o email "pauodriguesna@gmail.com" e confirmo a senha "123456@@"
    E eu clico no botão "Crie uma conta"
    Então eu vejo a mensagem "Erro ao criar usuário. Talvez esse nome já esteja registrado..."

  # Cenário 3: Registro com problemas de senha
  Cenário: Usuário tenta se registrar com senhas que não correspondem
    Dado que estou registrando uma conta única
    Quando eu preencho o formulário de registro com uma senha e confirmação diferentes
    E eu clico no botão "Crie uma conta"
    Então eu vejo a mensagem "Senhas não batem"


  # Cenário 4: campos faltando
  Cenário: Usuário tenta se registrar deixando campos obrigatórios vazios
    Dado que estou registrando uma conta única
    Quando eu deixo alguns campos obrigatórios do formulário de registro vazios
    Então eu devo ver o botão de criar conta desativado

  # Cenário 5: Senha com menos de 5 digitos
  Cenário: Usuário tenta se registrar com uma senha fraca
    Dado que estou registrando uma conta única
    Então eu preencho o nome de usuário "Anamaro1", a senha "123", o email "pauodriguesna@gmail.com" e confirmo a senha "123"
    E eu clico no botão "Crie uma conta"
    Então eu vejo a mensagem "Senha inválida. Precisa pelo menos 5 caracteres."
