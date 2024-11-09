
    #Cenário 1: Verificar os gastos planejados, empenhados e liquidados de uma determinada despesa pela tabela. O usuário tem certeza que tal despesa existe.
    Então('eu clico em {string} na tabela de distribuição de recursos') do |despesa|
        existe_despesa = false #variável booleana
        numPagina = 1 #variável que armazena o número da próxima página a ser vasculhada
        sleep 3 #3 segundos adicionais para carregar  página
        loop do #loop para procurar em todas as páginas caso não encontre.
            if page.has_content?(despesa) # Procura a despesa na lista
                existe_despesa = true
                first('a', text: despesa).click #clicou na despesa encontrada
                expect(existe_despesa).to be true #linha para concluir o cenário
                break;
            else
                existe_despesa = false
            end
            unless existe_despesa #se não encontrou a despesa procura na próxima página
                within('ul.inline-flex.-space-x-px') do #procura no elemento que tem os botões para mudar de página
                    if page.has_css?('a[role="button"]', text: (numPagina + 1).to_s) # Verifica se existe o botão da próxima página
                        find('a[role="button"]', text: (numPagina + 1).to_s).click #se existir clica e muda de página, retornando ao início do loop
                        numPagina += 1 #procura na próxima página caso não encontre novamente
                    else
                        expect(existe_despesa).to be true #serve para falhar o teste caso não encontre a despesa na lista (erro de banco de dados ou sei lá)
                        break #acabaram as páginas e não encontrou a despesa
                    end
                end
            end
        end
    end
    
    E('eu deveria ver as despesas de {string}') do |despesa|
        expect(page).to have_content(despesa)
        expect(page).to have_content("R$")
    end                
    
    #Cenário 2: Verificar os gastos planejados, empenhados e liquidados de uma determinada despesa que não está na tabela.
    Então('eu procuro {string} na tabela de distribuição de recursos') do |despesa|
        existe_despesa = false #variável booleana
        numPagina = 1 #variável que armazena o número da próxima página a ser vasculhada
        sleep 3 #3 segundos adicionais para carregar  página
        loop do #loop para procurar em todas as páginas caso não encontre.
            if page.has_content?(despesa) # Procura a despesa na lista
                existe_despesa = true
                expect(existe_despesa).to be false #linha para concluir o cenário
                break;
            else
                existe_despesa = false
            end
            unless existe_despesa #se não encontrou a despesa procura na próxima página
                if page.has_css?('a[role="button"]', text: (numPagina + 1).to_s) # Verifica se existe o botão da próxima página
                    find('a[role="button"]', text: (numPagina + 1).to_s).click #se existir clica e muda de página, retornando ao início do loop
                    numPagina += 1 #procura na próxima página caso não encontre novamente
                else
                    expect(existe_despesa).to be false #serve para concluir o teste caso não encontre a despesa na lista (sucesso)
                    break #acabaram as páginas e não encontrou a despesa
                end
                #end
            end
        end
    end

    E('eu não deveria encontrar {string}') do |despesa|
        expect(page).not_to have_content(despesa)
    end

 
    