<template>
  <div class="pg-about pb-20">
    <div class="md:container mx-auto pt-20">
      <div class="row grid grid-cols-5 gap-4">
         <div class="column border-r-2 pl-5 mt-2">
          <div class="pg-about__content text-neutral-light">
            <h4 class="text-lg font-bold mb-2">Implementado por:</h4>
            <ul>
              <li class="">Fernando Ferreira Diniz de Moraes</li>
              <li>Profª. Drª. Gisele da Silva Craveiro</li>
              <li>
                <a
                  class="underline text-secondary-base"
                  href="https://ikotema.digital/andres/"
                  target="_blank"
                  >Andrés M. R. Martano</a
                >
              </li>
              <li>Sol Lima</li>
              <li>Alexandre Souza</li>
              <li>Renan de Sousa Ferreira</li>
              <li>
                <a
                  class="underline text-secondary-base"
                  href="https://github.com/vanessa-nascimento"
                  target="_blank"
                  >Vanessa Alves do Nascimento</a>
              </li>
            </ul>
            <h4 class="text-lg font-bold my-2">Colaboração:</h4>
            <ul>
              <li>Prof. Dr. Jorge A. S. Machado</li>
              <li>Dra. Jutta Schmidt Machado</li>
              <li>Tamiris de Jesus</li>
              <li>Peter Krauss</li>
            </ul>
          </div>
        </div>
        <div class="column col-span-4">
          <h1 class="pg-about__title text-neutral-base text-4xl font-bold">
            Cuidando do Meu Bairro
          </h1>
          <div class="pg-about__content text-neutral-light text-lg mt-2">
            <p>Buscando contribuir na legibilidade da informação orçamentária ao público, o projeto Cuidando do Meu Bairro apresenta dados de execução orçamentária no mapa da cidade de São Paulo através da geocodificação, a fim de aproximar a cidadania ao acompanhamento em tempo real dos gastos públicos na cidade de São Paulo. A plataforma Cuidando do Meu Bairro (CMB), que em 2022 completa 10 anos de operação, recebeu a menção honrosa do Prêmio Luís Fernando de Computação, veja a notícia <a
                class="underline text-secondary-base"
                href="http://www5.each.usp.br/noticias/projeto-cuidando-do-meu-bairro-recebe-mencao-honrosa-no-premio-luiz-fernando-de-computacao/"
                target="_blank"
                >aqui</a
              >.</p>
            <p class="text-neutral-base mt-5">
              Acesse nosso blog clicando
              <a
                class="underline text-secondary-base"
                href="https://colab.each.usp.br/blog/tag/cuidando-do-meu-bairro/"
                target="_blank"
                >aqui</a
              >.
            </p>
            <p class="text-neutral-base">
              Caso queira contribuir com nosso projeto, acesse o nosso
              <a
                class="underline text-secondary-base"
                href="https://gitlab.com/cuidandodomeubairro"
                target="_blank"
                >Gitlab</a
              >.
            </p>
            <p class="text-neutral-base">
              Para entrar em contato conosco, pode nos enviar um e-mail:
              <a
                class="underline text-secondary-base"
                href="mailto:ola@cuidando.vc"
                >ola@cuidando.vc</a
              >.
            </p>
          </div>
        </div>
       
      </div>
      <div class="row">
        <partners />
      </div>
    </div>
  </div>
</template>

<script>
import Partners from "@/components/Partners.vue";

export default {
  components: { Partners },
};
</script>

<style scoped></style>
