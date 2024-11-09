# Cuidando do Meu Bairro GP6


## Badges

<a href="https://codeclimate.com/github/Phar187/cuidando-do-meu-bairro-gp6/maintainability"><img src="https://api.codeclimate.com/v1/badges/d9ff8f1ba8e807f6991d/maintainability" /></a>

[![Setup and Run Project](https://github.com/Phar187/cuidando-do-meu-bairro-gp6/actions/workflows/main.yml/badge.svg)](https://github.com/Phar187/cuidando-do-meu-bairro-gp6/actions/workflows/main.yml)


## Configuração e Execução


Configuração do ambiente Ubuntu (Linux) para rodar a interface `website-vuejs`:


### 1. Clonar o repositório


- Abra o terminal `(Ctrl + Alt + T)`
- Clone este repositório:

```bash
git clone https://github.com/Phar187/cuidando-do-meu-bairro-gp6.git
```


### 2. Instalar o Python 2.7


- Instale esta versão do python:

```bash
sudo apt install python2.7 -y
```


### 3. Instalar Node.js (versão 14) usando NVM


- Para gerenciar diferentes versões do Node.js, é recomendado usar o gerenciador NVM
- Primeiro, instale o `nvm`:

```bash
curl -o- <https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh> | bash
```

- Carregue o `nvm` no terminal:

```bash
source ~/.bashrc
```

- Instale a versão 14 do Node.js:

```bash
nvm install 14
nvm use 14
```


### 4. Instalando as dependências do projeto


- Entre no diretório do projeto clonado:

```bash
cd website-vuejs
```

- Instale todas as dependências do projeto:

```bash
npm install
```

- Instale pacotes adicionais necessários para o projeto:

```bash
npm install leaflet vue2-leaflet
```

### 5. Executar o projeto


- Para inicar o projeto, execute:

```bash
npm run serve
```


Obs.: Pode ser que aparecça uma mensagem de erro devido ao endpoint de dados estar indisponível (erro 400), especialmente se estiver rodando localmente. Esse alerta pode ser ignorado clicando no "X"



## Testes de unidade 



## Colaboradores
**Paulo Rodrigues 13671914** - ajudou na construção dos testes de aceitação de login, registro e blog, resolução das dependências dos testes unitários.


**Laís da Silva Moreira 13838482** - ajudou na construção dos testes de aceitação das atividades recentes do site, que englobam o acompanhamento de despesas específicas e seus detalhes.

**Samuel Barbosa Azevedo** - implementou os testes de unidade, pesquisou como configurar os ambientes para rodar as ferramentas e participou ativamente no desenvovimento das ideias para os testes.

**Bruno Arnone Franchi 13748040** - ajudou na construção dos testes de aceitação de todos os links presentes na página sobre, e de todas as funcionalidades e do gráfico presentes na página análises.


**Aline da Costa Santos 11918821** - fez os testes de aceitação sobre a edição de perfil, que inclui edição da senha, email e descrição, e também os testes sobre a visualização do mapa.

**Marcos Vinicius Silva de Souza 13695132** - implementou o teste de aceitação “Visualização e Acompanhamento de Gastos por Instituição” e criou 3 novas funcionalidades para o website-vuejs, as quais estão descritas com detalhes mais abaixo.

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

É recomendado executar cada teste individualmente para análise detalhada, e para evitar erros.

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

### Novas funcionalidades implementadas

Foram adicionadas 3 novas funcionalidades:
   1- Alteração do arquivo "router.js" (website-vuejs/src/router.js) para redirecionar o usuário para o ano atual caso a URL não esteja especificando (antes 2022 era o padrão).
   2- Alteração do arquivo "Home.vue" (website-vuejs/src/views/Home.vue). O botão "BAIXAR TABELA" agora baixa diretamente a tabela do ano correspondente presente na URL, ao invés de redirecionar o usuário à página de downloads das tabelas.
   3- Novamente, alteração do arquivo "Home.vue" (website-vuejs/src/views/Home.vue). Foi adicionado outro botão chamado "OUTRAS TABELAS" logo ao lado do botão "BAIXAR TABELA" que herda o comportamento antigo de redirecionar o usuário para a página de downloads da tabela de gastos.

--- 


