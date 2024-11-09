# Cuidando do Meu Bairro GP6


## Badges

<a href="https://codeclimate.com/github/Phar187/cuidando-do-meu-bairro-gp6/maintainability"><img src="https://api.codeclimate.com/v1/badges/d9ff8f1ba8e807f6991d/maintainability" /></a>

[![Setup and Run Project](https://github.com/Phar187/cuidando-do-meu-bairro-gp6/actions/workflows/main.yml/badge.svg)](https://github.com/Phar187/cuidando-do-meu-bairro-gp6/actions/workflows/main.yml)


## Configuração e Execução



## Testes de unidade 



## Colaboradores
**Paulo Rodrigues 13671914** - ajudou na construção dos testes de aceitação de login, registro e blog, resolução das dependências dos testes unitários.


**Laís da Silva Moreira 13838482** - ajudou na construção dos testes de aceitação das atividades recentes do site, que englobam o acompanhamento de despesas específicas e seus detalhes.


**Bruno Arnone Franchi 13748040** - ajudou na construção dos testes de aceitação de todos os links presentes na página sobre, e de todas as funcionalidades e do gráfico presentes na página análises.


## Testes de Aceitação

Este documento descreve os testes de aceitação para as principais funcionalidades do sistema, incluindo instruções de execução e a organização dos arquivos de teste.

### Estrutura dos Testes

As funcionalidades foram separadas conforme as principais ações do site. Cada funcionalidade possui um arquivo `.feature` correspondente na pasta `features`:

- **Acesso às Informações de Gastos**
- **Login e Autenticação** 
- **Cadastro de Usuários** 
- **Edição de Perfil de Usuário**
- **Atividades Recentes**
- **Acompanhamento de Gastos por Instituição**
- **Verificação de Mudanças no Gráfico da Página Análises** 
- **Verificação de Links na Página Sobre** 
- **Acesso à Página do Blog**

Para simplificar a estrutura, as funcionalidades de login, cadastro e edição de perfil compartilham um único arquivo de steps, evitando redundâncias e facilitando a manutenção dos testes.

### Execução dos Testes

Os arquivos `.feature` podem ser executados individualmente usando:

```bash
cucumber features/nome_do_arquivo.feature
```

Para rodar todos os testes de uma vez, utilize apenas `cucumber`, embora seja recomendado executar cada teste individualmente para análise detalhada.

### Considerações sobre os Testes

- **Acompanhamento de Gastos por Instituição**: A busca na tabela pode ser lenta dependendo do termo pesquisado. para o cenário 01, usamos um termo aleatório, e como eles não seguem uma ordem de exibição, o tempo de verificação pode variar a cada teste, enquanto o cenário 02 simula uma busca por algo inexistente, exigindo uma verificação completa e lenta da tabela. Recomenda-se rodar este teste (`cucumber features/acompanhamento_gastos.feature`) por último.

### Funcionalidades Problemáticas

Algumas funcionalidades não possuem testes de aceitação completos devido a limitações técnicas:

1. **Busca no Mapa**: A busca por bairro no mapa não está funcional, impossibilitando testes de aceitação para essa área.

2. **Links Ambíguos na Página Sobre**: Links apontando para "aqui" são confusos e não indicam claramente o destino, dificultando a execução de testes consistentes. Idealmente, esses links deveriam ser mais descritivos.

3. **Edição de Perfil**: Há limitações que comprometem a validade dos testes:
   - **Botão de Editar Descrição**: Não funcional, impedindo o teste de edição de descrição.
   - **Validação de Senha**: O sistema não avisa se a senha atual está correta ou não, de modo que apesar da senha não ser alterada por preencher a atual erroneamente, não é eexplicitado ao usuário. 
   - **Validação de Email**: Emails inválidos não são rejeitados explicitamente, o sistema simplesmente não altera o email.

### Considerações sobre os testes de aceitação 

Os testes de aceitação cobrem as funcionalidades principais e operacionais do sistema. Problemas de funcionamento ou validações ausentes foram documentados para futuras correções, com o objetivo de garantir testes completos e funcionais quando as melhorias forem implementadas.

--- 


