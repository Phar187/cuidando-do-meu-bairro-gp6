<template>
  <li class="top-bar py-5 border-b border-gray-100 text-neutral-base">
      <div class="row grid grid-cols-6 gap-1">
          <div class="description mr-4 col-span-5 flex">
              <div class="icon w-20 mr-4">
                  <img class="icon" :src="$assets.aPer">
              </div>
              <div>
                <div :class="{ '': true, '': !showRespostas }">
                    {{ pedido.description }}
                </div>
                <div v-if="showRespostas" class="mt-5">
                  <div class="py-5 border-y border-gray-200 mb-5">
                    <p><b>Protocolo:</b> {{ pedido.protocol }}</p>
                    <p><b>Órgão:</b> {{ pedido.orgao_name }}</p>
                  </div>
                  <div v-if="pedido.attachments.length">
                      <h3 class="font-semibold text-lg">Anexos</h3>
                      <ul>
                          <li v-for="(attachment, i) in attachments" :key="i">
                              <a :href="attachment.ia_url" target="_blank">{{ attachment.name }}</a>
                          </li>
                      </ul>
                  </div>
                  <h3 class="font-semibold text-lg">Respostas</h3>
                  <ul class="list-bare pt-3">
                      <li class="border-b border-gray-100 py-2" v-for="(item, i) in pedido.history" :key="i">
                          <div v-if="item.date">
                              <b>{{ $t('Date') }}:</b> {{ formatDate(item.date) }}
                          </div>
                          <div v-if="item.responsible">
                              <b>{{ $t('Responsible') }}:</b> {{ item.responsible }}
                          </div>
                          <div v-if="item.situation">
                              <b>{{ $t('State') }}:</b> {{ item.situation }}
                          </div>
                          <p>{{ item.justification }}</p>
                      </li>
                  </ul>
                  <p v-if="!pedido.history.length">Não há resposta</p>
                </div>
              </div>
          </div>
          <div class="date text-right">
              <div class="row">
                  <div class="col-xs-6">
                    <p>{{ pedido.request_date ? formatDate(pedido.request_date) : '' }}</p>
                    
                  </div>
                  <div class="col-xs-6">
                      <router-link class="underline text-secondary-base cursor-pointer" :to="{ name: 'pessoa', params: { viewingUser: pedido.author } }">
                        {{ pedido.author }}
                      </router-link>
                  </div>
              </div>
          </div>
      </div>
      <div class="mt-4 flex items-center justify-between">
      <div>
        <button
          v-if="pedido.allow_recurso && username === pedido.author"
          @click="openModal('recurso')"
          class="btn btn-color-sec relative text-right text-white px-3 py-2 cursor-pointer bg-secondary-light font-light hover:bg-secondary-base rounded"
        >
          {{ $t('Appeal') }}
          <span class="right-arrow"/>
        </button>

        <button-spinner
          type="submit" v-if="!subscriptions[pedido.notification_id]"
          @click.prevent.native="subscribe({ tag: pedido.notification_id, author: pedido.notification_author })"
          :condition="pending.subscribe[pedido.notification_id]"
          class="btn btn-color-sec relative text-right text-white px-3 py-2 cursor-pointer bg-secondary-light font-light hover:bg-secondary-base rounded"
        >
            {{ $t("Follow question") }}
        </button-spinner>

        <button-spinner
          type="submit" v-else
          @click.prevent.native="unsubscribe({ tag: pedido.notification_id })"
          :condition="pending.unsubscribe[pedido.notification_id]"
          class="btn btn-color-sec relative text-right text-white px-3 py-2 cursor-pointer bg-secondary-light font-light hover:bg-secondary-base rounded"
          >
            {{ $t("Unfollow question") }}
        </button-spinner>
      </div>
      <div class="text-right"
        v-if="!showRespostas"
      >
          <a @click="showRespostas = true" class="underline text-secondary-base cursor-pointer inline-flex items-center">
              {{ pedido.history.length }}
              {{ pedido.history.length-1 > 1 ? $t('Respostas') : $t('Resposta') }}
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 17l-4 4m0 0l-4-4m4 4V3"></path></svg>
          </a>
      </div>
      <div v-else>
          <a @click="showRespostas = false" class="underline text-secondary-base cursor-pointer inline-flex items-center">
              {{ $t('hide') }}
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7l4-4m0 0l4 4m-4-4v18"></path></svg>
          </a>
      </div>
    </div> 
  </li>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'
import { formatDate } from '@/utils'
export default {
  name: 'pergunta-pedido',
  props: {
    pedido: Object
  },
  components: {
  },
  data () {
    return {
      showRespostas: false
    }
  },
  computed: {
    ...mapState({
      subscriptions: state => state.subscriptions.subscriptions,
      pending: state => state.subscriptions.pending,
      username: state => state.auth.username
    })
  },
  methods: {
    formatDate,
    ...mapMutations(['openModal']),
    ...mapActions(['subscribe', 'unsubscribe'])
  }
}
</script>
