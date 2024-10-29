<template>
  <div class="perguntas">

    <div class="row flex items-center justify-between border-b border-gray-100 pb-5">
        <div class="">
            <h2 class="text-neutral-base font-semibold text-xl">{{ $t('want_to_question?') }}</h2>
            <p class="text-neutral-light">Essa pergunta será enviada diretamente ao órgão responsável via e-SIC</p>
        </div>

        <div class="new-perg-button text-right">
            <button 
              @click="username ? requireLogin : openModal('pergunta')"
              class="btn btn-color-sec relative text-right text-white px-3 py-2 cursor-pointer bg-secondary-light font-light hover:bg-secondary-base rounded">
              {{ $t('Make a question') }}
              <span class="right-arrow"
            />
            </button>
        </div>
    </div>

    <!-- Prepedidos -->
    <ul class="list-bare">
      <li class="top-bar" v-for="(prepedido, i) in pedidos.prepedidos" :key="i">
        <p><b>Pergunta enviada:</b> {{ prepedido.text }}</p>
      </li>
    </ul>

    <!-- Perguntas -->
    <ul class="list-bare">
      <pergunta-item v-for="(pedido, i) in pedidos" :key="i" :pedido="pedido"/>
    </ul>

    <modal-box modal-id="pergunta">
        <pergunta-form/>
    </modal-box>

    <modal-box modal-id="recurso">
        <recurso-form/>
    </modal-box>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'
import PerguntaItem from '@/components/perguntas/PerguntaItem.vue'
import PerguntaForm from '@/components/perguntas/PerguntaForm.vue'
import RecursoForm from '@/components/perguntas/RecursoForm.vue'

export default {
  name: 'perguntas-tab',
  components: {
    PerguntaItem,
    PerguntaForm,
    RecursoForm
  },
  computed: {
    ...mapState({
      pedidos: state => state.esic.pedidos,
      prepedidos: state => state.esic.prepedidos,
      username: state => state.auth.username,
    })
  },
  methods: {
    // TODO
    checkSubscribed () {
    },
    subscribe () {
    },
    openModalQuestion () {
      this.openModal('pergunta')
    },
    ...mapActions(['requireLogin']),
    ...mapMutations(['openModal'])
  }
}
</script>
