require 'capybara/cucumber'
require 'selenium-webdriver'

# Configuração do driver padrão para usar o Selenium com o navegador Chrome
Capybara.default_driver = :selenium_chrome



# Definindo o endereço do site que será testado
Capybara.app_host = 'https://cuidando.vc/2022/1'  # Substitua pela URL do site que você vai testar


# Configurar Capybara para usar o Chrome
Capybara.register_driver :selenium do |app|
  Capybara::Selenium::Driver.new(app, browser: :chrome, options: Selenium::WebDriver::Chrome::Options.new(binary: 'C:\Program Files\Google\Chrome\Application\chrome.exe'))
end

Before do
  unless @session_started
    visit('/')  # Visita a homepage apenas na primeira vez
    @session_started = true
  end
end



# Tempo máximo de espera para elementos dinâmicos carregarem na página
Capybara.default_max_wait_time = 6





# Configura o caminho para o ChromeDriver que você acabou de baixar
Selenium::WebDriver::Chrome::Service.driver_path = 'C:\Users\paulo\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'


