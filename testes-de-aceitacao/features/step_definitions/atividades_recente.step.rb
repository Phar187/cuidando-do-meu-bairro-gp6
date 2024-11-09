
# Cenário 1: verificando que a lista de atividades recentes está visível
Quando('procuro pelas atividades recentes do site') do
    # Verifica se a lista de atividades recentes está presente na página
    expect(page).to have_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div/div/ol', wait: 10)
  end
  
  Então('devo ver uma lista de atividades recentes com detalhes como data, título e status atual') do
    # Seleciona todos os itens de atividades recentes dentro da lista usando o xpath do <li>
    atividades = page.all(:xpath, '//*[@id="app"]/div/div[2]/div/div[3]/div/div/ol/li')
  
    # Garante que a lista de atividades não está vazia
    expect(atividades).not_to be_empty
  
    # Para cada atividade, verifica os detalhes principais: data, título e status
    atividades.each do |atividade|
      # Verifica se a data está presente
      expect(atividade).to have_xpath('.//time') 
      # Verifica se o título da atividade está presente
      expect(atividade).to have_xpath('.//span/div/h3') 
      # Verifica se o status da despesa está presente
      expect(atividade).to have_xpath('.//span/div/p') 
    end
  end
  
  
  # Cenário 2: procurando detalhes sobre uma atividade recente específica
  Quando('clico no botão "Saiba mais" de uma atividade específica') do
    # Localizando a atividade e i botão
    atividade = page.find(:xpath, '//*[@id="app"]/div/div[2]/div/div[3]/div/div/ol/li[1]')
    saiba_mais_botao = atividade.find(:xpath, './/span/div/a')
    saiba_mais_botao.click
  end
  
  Então('devo ser redirecionado para a página de detalhes da atividade') do
    # Verifica se a URL contém o prefixo esperado da página de detalhes da atividade
    expect(page.current_url).to match(%r{https://cuidando\.vc/despesa/\d+/\S+})
  end
  
  Então('devo ver informações detalhadas sobre a atividade selecionada') do
    # Localizando a div com os detalhes da atividade/despesa
    detalhes_despesa = page.find(:xpath, '//*[@id="app"]/div/div[2]/div[1]')
  
    # Descrição do programa em que a despesa faz parte
    expect(detalhes_despesa).to have_xpath('.//div[2]/div/div[1]/div/div[1]/h1')
  
    # Tipo de despesa
    expect(detalhes_despesa).to have_xpath('.//div[2]/div/div[1]/div/div[2]/h2')
  
    # Status da despesa
    expect(detalhes_despesa).to have_xpath('.//div[2]/div/div[2]/div[1]/span')
  end
  
  
  # Cenário 3: acompanhamento de despesa para monitoramento
  Dado('que estou na página sobre detalhes da atividade recente escolhida') do
    visit('https://cuidando.vc/despesa/2022/2024.180791.25.10.13.392.3001.33903900.90.39.0.8026')
    expect(page).to have_xpath('//*[@id="app"]/div/div[2]/div[1]', visible: true)
  end
  
  E('vejo o botão "Acompanhar despesa"') do
    # Localiza o botão e verifica seu texto atual
    acompanhar_despesa_botao = page.find(:xpath, '//*[@id="app"]/div/div[2]/div[1]/div/div/div/div[3]/div/button')
  
    # Se o botão já estiver em "Deixar de acompanhar despesa", clica para alterar para "Acompanhar despesa"
    if acompanhar_despesa_botao.text == 'Deixar de acompanhar despesa'
      acompanhar_despesa_botao.click
      # Verifica se o texto mudou para "Acompanhar despesa"
      expect(acompanhar_despesa_botao).to have_text('Acompanhar despesa')
    else
      expect(acompanhar_despesa_botao).to have_text('Acompanhar despesa')
    end
  end
  
  Quando('clico no botão "Acompanhar despesa"') do
    page.find(:xpath, '//*[@id="app"]/div/div[2]/div[1]/div/div/div/div[3]/div/button').click
  end
  
  Então('devo ver o botão "Deixar de acompanhar despesa"') do
    # verifica que o botão agora exibe o texto "Deixar de companhar despesa"
    deixar_acompanhar_botao = page.find(:xpath, '//*[@id="app"]/div/div[2]/div[1]/div/div/div/div[3]/div/button')
    expect(deixar_acompanhar_botao).to have_text('Deixar de acompanhar despesa')
  end
  
  
  # Cenário 4: procura por informações de despesa em JSON
  Dado('que estou na página sobre uma despesa específica') do 
    # Acessa diretamente a página de despesa específica
    visit('https://cuidando.vc/despesa/2022/2024.180791.25.10.13.392.3001.33903900.90.39.0.8026')
    expect(page).to have_xpath('//*[@id="app"]/div/div[2]/div[1]', visible: true)
  end
  
  E('vejo o botão "Mais informações"') do
    expect(page).to have_xpath('//*[@id="app"]/div/div[2]/div[1]/div/div/div/div[4]/div[3]/button', text: 'Mais informações')
  end
  
  Quando('clico no botão "Mais informações"') do
    mais_informacoes_botao = page.find(:xpath, '//*[@id="app"]/div/div[2]/div[1]/div/div/div/div[4]/div[3]/button')
    mais_informacoes_botao.click
  end
  
  Então('devo ver as informações da despesa em formato JSON') do
    json_content = page.find('#resultCode').text
    expect(json_content).to include('{')
    expect(json_content).to include('}')
  end