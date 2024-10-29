<template>
  <div class="pg-despesa bg-gray-50 -mt-2">
    <div class="pg-despesa__description">
      <div class="container-fluid">
        <div class="row">
          <div class="container mx-auto">
            <div class="row">
              <div class="pt-5">
                <router-link class="btn__back-to-year inline-flex text-sm items-center underline text-secondary-light" :to="{ name: 'home', params: { year } }">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
                  {{ $t('back to year') }}
                </router-link>
              </div>
            </div>
            <div class="row relative">
              <despesa-main/>
            </div>

            <div class="lg:flex justify-between border-t-2 border-gray-200 pt-10">
              <div class="c-acompanhar-despesa">
                <p class="text-neutral-base font-semibold text-xl">Acompanhe a despesa</p>
                <p class="text-neutral-light mb-3">Quer receber atualizações sobre movimentações dessa despesa?</p>
                <button-spinner
                type="submit" v-if="!subscriptions[pointInfo.notification_id]"
                @focus.native="requireLogin"
                @click.prevent.native="subscribe({ tag: pointInfo.notification_id, author: pointInfo.notification_author })"
                :condition="pending.subscribe[pointInfo.notification_id]"
                class="text-right text-white px-4 py-3 cursor-pointer bg-secondary-light font-light hover:bg-secondary-base rounded">
                {{ $t("Follow expense") }}
                </button-spinner>
                <button-spinner
                  type="submit" v-else
                  @click.prevent.native="unsubscribe({ tag: pointInfo.notification_id })"
                  :condition="pending.unsubscribe[pointInfo.notification_id]"
                  class="text-right text-white px-4 py-3 cursor-pointer bg-secondary-light font-light hover:bg-secondary-base rounded">
                  {{ $t("Unfollow expense") }}
                </button-spinner>
              </div>
              <div class="c-visao-rua lg:text-right" v-if="pointInfo && pointInfo.geometry">
                <p class="text-neutral-base font-semibold text-xl">Visão da Rua</p>
                <p class="text-neutral-light mb-5">Visualize como está o andamento da obra</p>
                <a class="bg-secondary-light text-white rounded font-light hover:bg-secondary-base py-3 px-4" :href="'https://www.instantstreetview.com/@' + pointInfo.geometry.coordinates[1] + ',' + pointInfo.geometry.coordinates[0] + ',0h,0p,1z'" target="_blank">Visão da rua</a>            
              </div>
            </div>
            <despesa-details/>
          </div>
        </div>
      </div>
    </div>
    <div class="pg-despesa__questions bg-white pb-16">
      <perg-com-tabs/>
    </div>
  </div>
  
</template>

<script>
import { mapState, mapActions } from 'vuex'
import DespesaDetails from '@/components/DespesaDetails.vue'
import DespesaMain from '@/components/DespesaMain.vue'
import PergComTabs from '@/components/PergComTabs.vue'
import FooterInfo from '../components/FooterInfo.vue'
export default {
  name: 'despesa-view',
  components: {
    DespesaMain,
    DespesaDetails,
    PergComTabs,
    FooterInfo
  },
  data () {
    return {

    }
  },
  computed: {
    ...mapState({
      subscriptions: state => state.subscriptions.subscriptions,
      pending: state => state.subscriptions.pending,
      pointInfo: state => state.money.pointInfo,
      code: state => state.route.params.code,
      year: state => state.route.params.year
    })
  },
  methods: {
    ...mapActions(['unsubscribe', 'subscribe', 'requireLogin'])
  }
}
</script>
