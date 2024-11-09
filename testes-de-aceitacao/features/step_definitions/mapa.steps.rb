E('eu vejo o mapa') do
    # Encontra a area do mapa
    mapa = find('#map-container') 

    # Verifica se o mapa está visível
    expect(mapa).to be_visible

    # Move o mouse até o centro do mapa
    mapa_hover = page.driver.browser.action.move_to(mapa.native).perform

    # Simula um clique no mapa
    mapa.double_click
end