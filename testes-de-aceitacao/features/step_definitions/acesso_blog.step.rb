#acesso a pagina blog
  Então('eu devo ser redirecionado para a página do Blog') do
    # Verifica se uma nova janela foi aberta com a URL do blog
    new_window = window_opened_by do
      find(:xpath, "//a[contains(@href, 'http://blog.cuidando.vc') and text()='Blog']", visible: true).click
    end
  
    within_window new_window do
      expect(current_url).to eq('https://colab.each.usp.br/blog/tag/cuidando-do-meu-bairro/')
    end
  end