
Quando ('eu clico no botão para ir para a página "Análises"') do
    expect(page).to have_link("Análises", wait: 10)
    click_link "Análises"
end

Quando ('o botão ano está desabilitado pois já foi selecionado') do
    button = find('button.pg-analisys__control-buttons-btn', text: 'ano')
    expect(button).to be_disabled
end

Quando ('o botão mês está desabilitado pois já foi selecionado') do
    button = find('button.pg-analisys__control-buttons-btn', text: 'mês')
    expect(button).to be_disabled
end

Quando ('o botão dia está desabilitado pois já foi selecionado') do
    button = find('button.pg-analisys__control-buttons-btn', text: 'dia')
    expect(button).to be_disabled
end

Quando ('eu clico no botão marcado como ano') do
    find('button.pg-analisys__control-buttons-btn', text: 'ano').click
end

Quando ('eu clico no botão marcado como mês') do
    find('button.pg-analisys__control-buttons-btn', text: 'mês').click
end

Quando ('eu clico no botão marcado como dia') do
    find('button.pg-analisys__control-buttons-btn', text: 'dia').click
end

Quando('o botão ano está habilitado') do
    button = find('button.pg-analisys__control-buttons-btn', text: 'ano')

    # Verifica se o botão está visível
    expect(button).to be_visible

    # Verifica se o botão está habilitado com base no atributo 'disabled'
    expect(button[:disabled]).to eq("false")
end

Então('o gráfico deve estar organizado por ano') do
    # Recupera todos os elementos tspan da página
    tspan_elements = page.all('tspan') # Seleciona todos os elementos tspan

    # Define o formato aceito para ano (de 1 a 4 dígitos)
    formato_ano = /^\d{1,4}$/

    # Cria um array de textos dos tspan que correspondem ao formato de ano
    anos_encontrados = tspan_elements.map(&:text).select { |texto| texto.match(formato_ano) }

    # Verifica se todos os tspan encontrados têm o formato de ano
    anos_encontrados.each do |ano|
        expect(ano).to match(formato_ano)
    end

    # Adicionalmente, você pode querer garantir que não existam outros formatos
    tspan_elements.each do |tspan|
        expect(tspan.text).to satisfy { |texto| texto.match(formato_ano) || texto.empty? }
    end
end

Então('o gráfico deve estar organizado por mês') do
    # Define o formato aceito para mês e ano
    formato_mes_ano = /^(Jan|Fev|Mar|Abr|Mai|Jun|Jul|Ago|Set|Out|Nov|Dez) \d{4}$/
    formato_numero = /^\d{1,3}$/ # Aceita números com até 3 dígitos

    retries = 3
    begin
        # Espera até que os elementos tspan estejam disponíveis
        expect(page).to have_css('tspan', wait: 10)

        # Recupera todos os elementos tspan da página novamente
        tspan_elements = page.all('tspan')

        # Filtra os elementos válidos
        valid_tspan_elements = tspan_elements.select do |tspan|
            tspan.text.match?(formato_mes_ano) || tspan.text.match?(formato_numero)
        end

        # Debug: imprime os textos dos tspan válidos
        puts valid_tspan_elements.map(&:text)

        # Verifica se todos os tspan encontrados têm o formato de mês/ano ou numérico
        valid_tspan_elements.each do |tspan|
            expect(tspan.text).to match(formato_mes_ano).or match(formato_numero)
        end

        # Adicionalmente, verifica que não existam outros formatos
        tspan_elements.each do |tspan|
            expect(tspan.text).to satisfy { |texto| texto.match(formato_mes_ano) || texto.match(formato_numero) || texto.empty? }
        end
    rescue Selenium::WebDriver::Error::StaleElementReferenceError
        retries -= 1
        if retries > 0
            sleep 1 # Espera 1 segundo antes de tentar novamente
            retry
        else
            raise
        end
    end
end

Então('o gráfico deve estar organizado por dia') do
    attempts = 0
    max_attempts = 5

    begin
        # Espera até que os elementos tspan estejam disponíveis
        expect(page).to have_css('tspan', wait: 10)

        # Recupera todos os elementos tspan da página novamente
        tspan_elements = page.all('tspan')

        # Debug: imprime os textos dos tspan
        puts tspan_elements.map(&:text)

        # Define o formato aceito para dia, mês e ano ou números de até 3 dígitos
        formato_dia_mes_ano = /^(0[1-9]|[12]\d|3[01]) (Jan|Fev|Mar|Abr|Mai|Jun|Jul|Ago|Set|Out|Nov|Dez) \d{4}$/
        formato_numerico = /^\d{1,3}$/

        # Verifica se todos os tspan encontrados têm o formato esperado ou estão vazios
        tspan_elements.each do |tspan|
            expect(tspan.text).to satisfy { |texto| texto.match(formato_dia_mes_ano) || texto.match(formato_numerico) || texto.empty? }
        end

        # Garante que todos os tspan estão no formato correto, numérico ou estão vazios
        expect(tspan_elements.size).to eq(tspan_elements.select { |tspan| tspan.text.match(formato_dia_mes_ano) || tspan.text.match(formato_numerico) || tspan.text.empty? }.size)

    rescue Selenium::WebDriver::Error::StaleElementReferenceError
        attempts += 1
        if attempts < max_attempts
            sleep 0.5 # Pequena pausa antes de tentar novamente
            retry
        else
            raise # Lança a exceção se o número máximo de tentativas for alcançado
        end
    end
end