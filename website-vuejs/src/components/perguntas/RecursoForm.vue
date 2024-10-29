<template>
    <div class="modal-body modal-body p-6 pb-4 lg:px-8 sm:pb-6 xl:pb-8">
        <h2 class="text-xl font-semibold text-neutral-base">Recorrer</h2>

        <p class="text-base text-neutral-base my-4">Aqui você tem como enviar seu recurso a respeito do gasto. Lembre-se que tanto sua pergunta como a resposta que vai receber do órgão público responsável serão compartilhadas aqui nesse site para todas as pessoas que estiverem interessadas. Para aumentar as chances de receber uma resposta satisfatória, elabore sua recurso levando em conta algumas dicas, veja <a class="underline text-secondary-light" href="http://cafehacker.prefeitura.sp.gov.br/wp-content/uploads/2014/09/cartilha_acessoainfosp.pdf" target="_blank">aqui</a> algumas delas.</p>

        <form class="form">
            <div class="form-group">
                <label class="sr-only" for="new-recurso-textarea">
                    {{ $t('Question') }}
                </label>
                <textarea id="new-recurso-textarea"
                    class="form-control bg-white border border-gray-300 text-neutral-base text-sm rounded-lg focus:ring-primary-dark focus:border-primary-dark block w-full p-2.5" 
                    :maxlength="maxPedidoLength"
                    rows="5"/>
                    <p>{{ $t('Remaining characters') }}: {{ remainingChars }}</p>
            </div>
            <button-spinner type="submit"
                    @click.prevent.native="sendRecurso({ key: $route.params.code, orgao, text })"
                    class="w-full mt-5 text-white cursor-pointer bg-secondary-light hover:bg-secondary-base focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center">
                {{ $t("Send") }}
            </button-spinner>
        </form>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  name: 'recurso-form',
  data () {
    return {
      text: '',
      maxPedidoLength: 5000
    }
  },
  computed: {
    remainingChars () {
      return this.maxPedidoLength - this.text.length
    },
    ...mapState({
      pointInfo: state => state.money.pointInfo
    })
  },
  methods: {
    ...mapActions([
      'sendRecurso'
    ])
  }
}
</script>
