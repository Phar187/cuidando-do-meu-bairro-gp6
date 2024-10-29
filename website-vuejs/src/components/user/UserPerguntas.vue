<template>
  <div v-if="userPerguntas.length">
    <div class="w-full mb-5 bg-white rounded-lg border border-gray-200 shadow-md p-5">
      <h2 class="text-neutral-base text-2xl font-bold mb-5">Perguntas Feitas</h2>
      <li class="p-5 border-b border-gray-200 text-neutral-base" v-for="pergunta in userPerguntas" :key="pergunta.protocolo">
        <router-link class="underline text-secondary-base" :to="routeToDespesa(pergunta.keywords[0])">
          {{ pergunta.protocolo }} - {{ pergunta.orgao }} - {{ pergunta.situacao }}
        </router-link>
      </li>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'user-perguntas',
  computed: {
    ...mapState({
      userPerguntas: state => state.esic.userPerguntas
    })
  },
  methods: {
    routeToDespesa (keyword) {
      return {
        name: 'despesa',
        params: {
          year: keyword.slice(0, 4),
          code: keyword
        }
      }
    }
  }
}
</script>
