
#arquivo de steps para atividades de login, registro, editar perfil 
Dado('que estou na página inicial') do
  visit('/')  # Navega para a página inicial
end

Quando('eu clico no link "Entrar" no menu') do
  within('nav.c-navbar.w-full.h-16.flex.items-center.bg-primary-base.fixed') do
    expect(page).to have_css('.px-4.mx-1.cursor-pointer.py-2.border.border-white', visible: true, wait: 50)
    find('.px-4.mx-1.cursor-pointer.py-2.border.border-white', wait: 40).click
  end
end

Então('o formulário de login aparece') do
  expect(page).to have_css('form.form.px-6.pb-4.lg\\:px-8.sm\\:pb-6.xl\\:pb-8', wait: 20)
end

Quando('eu preencho o nome de usuário {string} e a senha {string}') do |username, password|
  fill_in 'Nome de usuário', with: username
  fill_in 'Senha', with: password
end

Quando('eu clico no botão "Entrar"') do
  click_button 'Entrar'
end

Então('eu devo ver o perfil do usuário {string}') do |username|
  expect(page).to have_xpath("//button[contains(@class, 'text-white') and contains(text(), '#{username}')]", visible: true)
  page.find(:xpath, "//button[contains(@class, 'text-white') and contains(text(), '#{username}')]", visible: true).click
end

Então('eu devo ver a mensagem de nome de usuário inválido {string}') do |error_message|
  expect(page).to have_css('.px-6.pb-4.lg\\:px-8.sm\\:pb-6.xl\\:pb-8.text-sm.text-red-600')
  expect(page).to have_content(error_message)
end

Então('eu devo ver a mensagem de senha inválida {string}') do |error_message|
  expect(page).to have_content(error_message)
end

Quando('eu clico na opção "esqueceu a senha?"') do
  page.find(:xpath, "//a[contains(@class, 'text-primary-base') and contains(text(), 'Esqueceu a senha?')]").click
end

Então('eu devo ver um campo para inserir meu email') do
  expect(page).to have_xpath("//input[@id='login-form-email' and @type='email']", visible: true)
end

Quando('eu preencho o nome de usuário {string} e o email {string}') do |username, email|
  fill_in 'Nome de usuário', with: username
  fill_in 'login-form-email', with: email
end

Quando('eu clico no botão "Solicitar código"') do
  page.find(:xpath, "//button[contains(@class, 'btn') and contains(normalize-space(.), 'Solicitar código')]", visible: true).click
end

Quando('eu clico na opção "Crie uma conta"') do
  page.find(:xpath, "//a[contains(@class, 'text-primary-base') and contains(text(), 'Crie uma conta')]").click
end

Então('eu preencho o nome de usuário {string}, a senha {string}, o email {string} e confirmo a senha {string}') do |username, password, email, confirmed_password|
  fill_in 'Nome de usuário', with: username
  fill_in 'Senha', with: password
  fill_in 'login-form-email', with: email
  fill_in 'Confirmar Senha', with: confirmed_password
end

E('eu clico no botão "Crie uma conta"') do
  page.find(:xpath, "//button[contains(@class, 'btn') and not(@disabled)]//span[contains(text(), 'Crie uma conta')]").click
end

Então('eu vejo a mensagem {string}') do |error_message|
  expect(page).to have_xpath("//p[contains(@class, 'px-6') and contains(text(), '#{error_message}')]")
end

Então('eu não devo ver uma mensagem de erro') do
  expect(page).to have_no_xpath("//p[contains(@class, 'text-red-600') and contains(normalize-space(.), 'E-mail errado')]", wait: 10)
end

Então('eu devo ver a mensagem de erro {string}') do |error_message|
  expect(page).to have_xpath("//p[contains(@class, 'text-red-600') and contains(text(), '#{error_message}')]", wait: 10)
end

# Edição de Perfil

Então('o botão de editar a descrição existe') do
  expect(page).to have_selector("div.text-neutral-light.text-base.mt-2 button", text: "Editar")
end

Quando('eu clico no botão de editar o e-mail {string}') do |botao_texto|
  buttons = all('button', text: botao_texto)
  buttons[1].click if buttons.size > 1
end

E('eu vejo um formulário de email') do
  expect(page).to have_css('div.form-group.form')
end

E('eu insiro o novo e-mail {string}') do |novo_email|
  fill_in 'E-mail', with: ""
  fill_in 'E-mail', with: novo_email
end

E('eu clico no botão de salvar') do
  click_button 'Salvar'
end

Então('eu devo ver o e-mail atualizado como {string}') do |novo_email|
  expect(page).to have_content(novo_email, wait: 40)
end

Quando('eu clico no botão de editar senha {string}') do |botao_texto|
  buttons = all('button', text: botao_texto)
  buttons[2].click if buttons.size > 1
end

E('eu vejo um formulário de senha') do
  expect(page).to have_css('form.pessoa-edit-password-form')
end

E('eu insiro a senha atual {string}') do |senha_atual|
  fill_in 'Senha atual', with: senha_atual
end

Quando('eu insiro a nova senha {string}') do |nova_senha|
  fill_in 'Nova senha', with: nova_senha
end

Quando('eu confirmo a nova senha {string}') do |confirmacao_senha|
  fill_in 'Confime a nova senha', with: confirmacao_senha
end

Quando('eu clico no botão de salvar senha {string}') do |botao_texto|
  find('form.pessoa-edit-password-form button[type="submit"]', text: botao_texto).click
end

Então('eu vou para o perfil do usuário {string}') do |username|
  expect(page).to have_content("Informações pessoais")
  expect(page).to have_selector("button", text: "Editar", wait: 40)
end

# Passo para ver opções de perfil

E('eu devo ver as opções {string} e {string}') do |option1, option2|
  expect(page).to have_xpath("//a[contains(text(), '#{option1}')]", visible: true)
  expect(page).to have_xpath("//a[contains(text(), '#{option2}')]", visible: true)
end

Quando('eu clico no link {string}') do |link_text|
  page.find(:xpath, "//a[contains(text(), '#{link_text}')]", visible: true).click
end

Então("eu devo ver o nome do usuário {string} na barra de navegação") do |nome_usuario|
  within('nav.c-navbar') do
    expect(page).to have_content(nome_usuario)
  end
end

Quando('eu clico no botão com o nome de usuário {string}') do |nome_do_usuario|
  page.find(:xpath, "//button[contains(@class, 'text-white') and contains(normalize-space(text()), '#{nome_do_usuario}')]", visible: true).click
end

Então('eu não devo ver o perfil do usuário {string}') do |nome_do_usuario|
  expect(page).not_to have_selector('button', text: nome_do_usuario)
end



# Definição de dados unicos para registro
Dado('que estou registrando uma conta única') do
  # Gera um nome de usuário e email únicos usando o timestamp
  @username = "usuario_#{Time.now.to_i}"
  @password = 'SenhaSegura123'
  @confirm_password = 'SenhaSegura123'
  @unique_email = "usuario_#{Time.now.to_i}@exemplo.com"
end


Quando('eu preencho o formulário de registro com dados únicos') do
 
  fill_in 'Nome de usuário', with: @username
  fill_in 'login-form-email', with: @unique_email
  fill_in 'Senha', with: @password
  fill_in 'login-form-confirm-password', with: @confirm_password
end

# Novo step específico para verificar o perfil do usuário recém-registrado
Então('eu devo ver o perfil do usuário recém-registrado') do
  # Aqui, reutilizamos o step existente passando @username como argumento
  steps %(
    Então eu devo ver o perfil do usuário "#{@username}"
  )
end

Quando('eu preencho o formulário de registro com uma senha e confirmação diferentes') do
  fill_in 'Nome de usuário', with: @username
  fill_in 'login-form-email', with: @unique_email
  fill_in 'Senha', with: 'Senha123'
  fill_in 'login-form-confirm-password', with: 'SenhaDiferente'
end


Então('eu devo ver o botão de criar conta desativado') do
  # Verifica se o botão "Crie uma conta" está presente e desativado
  expect(page).to have_button('Crie uma conta', disabled: true)
end


Quando('eu deixo alguns campos obrigatórios do formulário de registro vazios') do
  fill_in 'Nome de usuário', with: @username
  fill_in 'login-form-email', with: ''  # Campo de email vazio
  fill_in 'Senha', with: @password
  fill_in 'login-form-confirm-password', with: ''  # Campo de confirmação de senha vazio
end


#parte das atividades recentes 
