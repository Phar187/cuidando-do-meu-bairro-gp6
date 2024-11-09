# Define uma variável global para armazenar a nova janela aberta em cada caso
$new_window = nil


Quando('eu clico no botão para ir para a página "Sobre"') do
    expect(page).to have_link("Sobre", wait: 10)
    click_link "Sobre"
end

Quando('clico no link Andrés M. R. Martano') do
    expect(page).to have_link("Andrés M. R. Martano", wait: 10)
    $new_window = window_opened_by { click_link "Andrés M. R. Martano" }
end

Quando('clico no link Vanessa Alves do Nascimento') do
    expect(page).to have_link("Vanessa Alves do Nascimento", wait: 10)
    $new_window = window_opened_by { click_link "Vanessa Alves do Nascimento" }
end

Quando('clico no link aqui para abrir a notícia') do
    expect(page).to have_link("aqui", wait: 10)
    $new_window = window_opened_by { click_link "aqui" }
end

Quando('clico no link aqui para abrir o blog') do
    expect(page).to have_link("aqui", wait: 10)
    $new_window = window_opened_by { click_link "aqui" }
end

Quando('clico no link Gitlab') do
    expect(page).to have_link("Gitlab", wait: 10)
    $new_window = window_opened_by { click_link "Gitlab" }
end

Então('deve abrir a página pessoal do colaborador Andrés M. R. Martano') do
    within_window $new_window do
        expect(page).to have_current_path('https://ikotema.digital/andres/')
    end
    $new_window.close
end

Então('deve abrir a página pessoal da colaboradora Vanessa Alves do Nascimento') do
    within_window $new_window do
        expect(page).to have_current_path('https://github.com/vanessa-nascimento')
    end
    $new_window.close
end

Então('deve abrir a página com a notícia do projeto') do
    within_window $new_window do
        expect(page).to have_current_path('http://www5.each.usp.br/noticias/projeto-cuidando-do-meu-bairro-recebe-mencao-honrosa-no-premio-luiz-fernando-de-computacao/')
    end
    $new_window.close
end

Então('deve abrir a página com o blog do projeto') do
    within_window $new_window do
        expect(page).to have_current_path('https://colab.each.usp.br/blog/tag/cuidando-do-meu-bairro/')
    end
    $new_window.close
end

Então('deve abrir a página com o repositório do projeto no Gitlab') do
    max_attempts = 5  # Define o número máximo de tentativas
    attempt = 0
  
    # Loop que tenta verificar a URL até o máximo de tentativas
    while attempt < max_attempts
      begin
        # Verifica se a URL atual é a esperada
        within_window $new_window do
          expect(page).to have_current_path('https://gitlab.com/cuidandodomeubairro')
        end
        
        # Fecha a janela se a verificação foi bem-sucedida
        $new_window.close
        break  # Sai do loop se a URL estiver correta
      rescue RSpec::Expectations::ExpectationNotMetError
        # Aguardamos um curto intervalo antes da próxima tentativa
        sleep 1
        attempt += 1
        # Levanta o erro se a última tentativa falhar
        raise 'Falha ao verificar a página do repositório no Gitlab' if attempt == max_attempts
      end
    end
  end
  