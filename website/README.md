# Website da plataforma Cuidando do Meu Bairro 2.0


## Instalando

Para instalar todos os repositórios necessários para executar esse projeto, há um shell script "guia" [aqui](doc/install.sh).

Caso só queira instalar esse repositório, clone-o e rode dentro dele:

```
$ npm i
```

Depois configure um `src/config.js`.


## Rodando

Para rodar o site:

```
$ npm run dev
```

Depois acesse `localhost:5001` em um navegador. Se quiser que o código atualize automaticamente conforme editar os arquivos, acesse `localhost:5001/webpack-dev-server/`.

Como o esse projeto depende de vários micro serviços, sugiro que você tenha um script para rodar todos eles quando quiser. Há um exemplo [aqui](doc/run.py).


## Compilando

Para compilar o site para produção, rode:

```
$ npm run dist
```

Caso queira usar um arquivo de configuração diferente do `config.js`, por exemplo um `config_prod.js`, passe a especificação desse arquivo através da variável de ambiente `CONFIG_FILE_ENV`. Para o arquivo `config_prod.js` ela deveria ser ajustada para `prod`. A seguinte linha rodaria o site localmente, mas usando a configuração de produção:

```
$ CONFIG_FILE_ENV=prod npm run dev
```

O site compilado (estático, com JS minificado etc) deverá estar na pasta `build`.
Você pode testá-lo entrando na pasta, servindo-o com o comando a seguir e abrindo o endereço em um navegador:

```
$ npm run viewdist
```


### Limitadores de versão do browser:

- [localStorage](http://caniuse.com/#feat=namevalue-storage): IE8+
- [history](http://caniuse.com/#feat=history): IE10+ (suporte manual minimamente implementado)
- Muitos outros...


A estrutura do código foi inspirada em: https://github.com/txchen/feplay/tree/gh-pages/riot_webpack
