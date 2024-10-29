<template>
  <div class="overflow-scroll">
    <div class="modal-body p-6 pb-4 lg:px-8 sm:pb-6 xl:pb-8">
        <h2 class="text-xl font-semibold text-neutral-base">O que deseja perguntar?</h2>

        <p class="text-base text-neutral-base my-4">Aqui você tem como enviar sua dúvida a respeito do gasto. Lembre-se que tanto sua pergunta como a resposta que vai receber do órgão público responsável serão compartilhadas aqui nesse site para todas as pessoas que estiverem interessadas. Para aumentar as chances de receber uma resposta satisfatória, elabore sua pergunta levando em conta algumas dicas, veja <a class="underline text-secondary-light" href="http://cafehacker.prefeitura.sp.gov.br/wp-content/uploads/2014/09/cartilha_acessoainfosp.pdf" target="_blank">aqui</a> algumas delas.
        </p>

        <div v-if="!bestFitOrgao" id="alert-4" class="flex p-4 mb-4 bg-yellow-100 rounded-lg" role="alert">
          <svg class="flex-shrink-0 w-5 h-5 text-yellow-700" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
          <div class="ml-3 text-sm font-medium text-yellow-700">
            <p>Ops... Parece que não conseguimos achar na lista do E-SIC o órgão responsável por essa despesa. Por favor, escolha um na lista abaixo.</p>
          </div>
          <button type="button" class="ml-auto -mx-1.5 -my-1.5 bg-yellow-100 text-yellow-500 rounded-lg focus:ring-2 focus:ring-yellow-400 p-1.5 hover:bg-yellow-200 inline-flex h-8 w-8" data-dismiss-target="#alert-4" aria-label="Close">
            <span class="sr-only">Fechar</span>
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
          </button>
        </div>

        <styled-select :options="orgaos" v-model="orgao"/>

        <h3 class="text-lg font-normal mt-4 text-neutral-base">Exemplo de pergunta</h3>
        <p class="text-base text-neutral-base my-4">{{ inicioPergunta }}</p>

        <form class="form">
            <div class="form-group">
              <label class="sr-only" for="new-pergunta-textarea">
                  {{ $t('Question') }}
              </label>
              <textarea id="new-pergunta-textarea"
                class="form-control bg-white border border-gray-300 text-neutral-base text-sm rounded-lg focus:ring-primary-dark focus:border-primary-dark block w-full p-2.5" 
                :maxlength="maxPedidoLength"
                v-model="text"
                rows="5"
              />
              <p class="text-gray-400 text-xs mt-2">{{ $t('Remaining characters') }}: {{ remainingChars }}</p>
            </div>
             <p class="text-base text-neutral-base my-4">Ao enviar o pedido, você deve estar de acordo com os <router-link class="underline text-secondary-base" to="/termos-de-uso" target="_blank">termos de uso</router-link>.</p>
            <button-spinner type="submit"
              @click.prevent.native="send"
              :condition="pending.sendingPergunta"
              :disabled="!text.length"
              class="w-full mt-5 text-white cursor-pointer bg-secondary-light hover:bg-secondary-base focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center"
              >
              {{ $t("Send") }}
            </button-spinner>
        </form>

       
    </div>
  </div>
    
</template>

<script>
import { mapState, mapActions, mapMutations } from 'vuex'
export default {
  name: 'pergunta-form',
  async mounted () {
    await Promise.all([this.getOrgaos(), this.getPointInfo({ params: { code: this.$route.params.code } })])
    // Initialize orgao var based on orgao in data
    if (!this.orgao && this.bestFitOrgao) this.orgao = this.bestFitOrgao
  },
  data () {
    return {
      text: '',
      maxPedidoLength: 5000,
      orgao: null
    }
  },
  computed: {
    remainingChars () {
      return this.maxPedidoLength - this.text.length
    },
    bestFitOrgao () {
      // If has a orgaos list
      if (this.orgaos) {
        // Tries to find the correct orgao for this despesa
        if (this.pointInfo) {
          for (let orgao of this.orgaos) {
            if (orgao.key.includes(this.pointInfo.ds_orgao.trim())) {
              return orgao.key
            }
          }
        }
      }
      return null
    },
    inicioPergunta () {
      return `Referente ao gasto público "${this.pointInfo.ds_projeto_atividade}", de ${this.pointInfo.cd_anoexecucao}, cujo órgão responsável é "${this.pointInfo.ds_orgao}", solicito informações:`
    },
    ...mapState({
      pointInfo: state => state.money.pointInfo,
      pending: state => state.esic.pending,
      orgaos: state => state.esic.orgaos
    })
  },
  methods: {
    async send () {
      await this.sendPergunta({
        keywords: [this.$route.params.code],
        orgao: this.orgao,
        text: this.inicioPergunta + ' ' + this.text
      })
      this.closeModal()
    },
    ...mapActions([
      'getPointInfo',
      'sendPergunta',
      'getOrgaos'
    ]),
    ...mapMutations(['closeModal'])
  }
}
</script>
