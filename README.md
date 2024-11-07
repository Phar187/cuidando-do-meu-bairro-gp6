# Cuidando do Meu Bairro GP6


## Badges

<a href="https://codeclimate.com/github/Phar187/cuidando-do-meu-bairro-gp6/maintainability"><img src="https://api.codeclimate.com/v1/badges/d9ff8f1ba8e807f6991d/maintainability" /></a>

[![Setup and Run Project](https://github.com/Phar187/cuidando-do-meu-bairro-gp6/actions/workflows/main.yml/badge.svg)](https://github.com/Phar187/cuidando-do-meu-bairro-gp6/actions/workflows/main.yml)


## Configuração e Execução



## Testes de unidade 



## Colaboradores



##Testes de Aceitação
Está descreve os testes de aceitação desenvolvidos para as principais funcionalidades do sistema, informações sobre como executar os testes e a organização dos arquivos.

#Estrutura dos Testes
As funcionalidades foram separadas de acordo com as principais ações esperadas no site. Cada funcionalidade tem um arquivo .feature correspondente dentro da pasta features, organizado da seguinte forma:

Acesso às Informações de Gastos
Login e Autenticação – Pronto
Cadastro de Usuários – Pronto
Edição de Perfil de Usuário
Atividades Recentes
Acompanhamento de Gastos por Instituição
Verificação das Mudanças do Gráfico na Página Análises – Pronto
Verificação do Funcionamento dos Links na Página Sobre – Pronto
Acesso à Página do Blog
Para simplificar a estrutura dos testes, as funcionalidades de login, cadastro e edição de perfil compartilham um único arquivo de steps, pois essas ações são interdependentes. Isso evita redundâncias e facilita a manutenção dos testes.

#Arquivos de Teste
Os arquivos .feature desenvolvidos estão organizados na pasta features e podem ser executados individualmente. eles podem ser executados da seguinte forma: 
cucumber features/nome_do_arquivo.feature ou apenas cucumber para rodar todos, mas não recomendo por não ser possível analisá-los com calma. 

#considerações sobre os testes 
1. Teste- Acompanhamento de Gastos por Instituição:o primeiro caso de teste em si faz uma busca na tabela pelo que foi passado nos cenários, então a depender do que é passado nele, caso esteja próximo ou não do topo, pode demorar, foi deixado uma pesquisa de um termo que está na primeira página. Já o segundo cenário considera uma busca por algo que não existe, então ele verifica toda a tabela, o que demora algum tempo, então recomendo usar o comando de teste dessa funcionalidade "cucumber features/acompanhamento_gastos.feature" por último. 

#funcionalidades problematicas
Algumas funcionalidades não possuem testes de aceitação devido a problemas técnicos ou limitações no próprio sistema:

1.Busca no Mapa:
A funcionalidade de busca por bairro no mapa atualmente não está funcionando, impedindo a criação de testes de aceitação para essa área específica do sistema.
Links Ambíguos na Página Sobre:

2.Links de paginas
Nos casos de links para a página do blog e a página de notícias do projeto, a interface do usuário apresenta links ambiguamente nomeados como "aqui", o que dificulta a identificação do destino esperado e impede a execução de testes de aceitação consistentes. Idealmente, esses links deveriam ter nomes descritivos que indiquem claramente o destino.
Problemas na Edição de Perfil:

3.Edição de perfil
Algumas limitações impedem testes de aceitação completos para a funcionalidade de edição de perfil:
Botão de Editar Descrição: Este botão não funciona, impossibilitando testes para editar a descrição do perfil.
Validação de Senha: Ao editar a senha, o sistema não verifica se a senha antiga está correta, o que permite trocas sem autenticação, afetando a validade dos testes.
Validação de Email: O sistema não verifica se o novo email é válido antes de salvar a alteração. Se o email não for válido, ele simplesmente não altera, o que impede uma validação eficaz via testes de aceitação.
Considerações Finais

Os testes de aceitação cobrem as funcionalidades principais que estão atualmente em pleno funcionamento. Problemas de funcionamento, como validação inadequada ou ausência de verificações necessárias, foram mencionados aqui, mas não podem ser testados completamente de forma plena até que as funcionalidades sejam corrigidas. Essas limitações nos testes foram observadas para futuras melhorias no sistema e garantir que, quando corrigidas, as funcionalidades possam ser testadas adequadamente.

