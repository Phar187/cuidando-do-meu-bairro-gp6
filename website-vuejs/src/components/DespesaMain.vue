<template>
  <div class="c-despesa-main">
    <div class="row">
        <div class="col-sm-12 my-3">
            <div class="c-despesa-main__program mb-5 flex flex-col justify-center items-center">
              <span class="text-secondary-base font-semibold text-center text-sm">{{ $t('Program') }}</span>
              <h1 class="c-despesa-main__title text-neutral-base text-center text-3xl font-bold">{{ this.pointInfo.ds_programa }}</h1>
            </div>
            <div class="c-despesa-main__program mb-10 flex flex-col justify-center items-center">
              <span class="text-secondary-base px-2 py-1 rounded font-semibold text-xs">{{ $t('Expense') }}</span>
              <h2 class="c-despesa-main__subtitle text-neutral-base text-2xl text-center font-light mt-1">{{ this.pointInfo.ds_projeto_atividade }}</h2>
            </div>
           <!-- <spinner class="dark-spinner" if="{ !this.pointInfo }" scale="0.25"/> -->
        </div>
    </div>
    <div>
      <div v-if="this.pointInfo" class="row flex justify-center items-center text-center">
        <span class="hidden fill-status-planejado fill-status-empenhado fill-status-liquidado"></span>
        <div v-for="(category, i) in categories" :key="i" class="flex justify-center items-center">
          <div class="col-sm-4 shadow-sm category px-16 py-7 rounded-full bg-white">
            <div v-if="category !== 'empenhado'" class="c-despesa-main__category-title text-neutral-base uppercase font-bold mb-4"> {{$t(category) }}</div>
            <div v-else class="c-despesa-main__category-title text-neutral-base uppercase font-bold mb-4"> {{$t(category) }}
              <span>
                <popper trigger="hover"
                :options="{
                  placement: 'top',
                  modifiers: { offset: { offset: '0,10px' } }
                }">
                  <div class="popper absolute">
                    Este valor corresponde a uma obrigação de pagamento da despesa pelo governo. Ele realiza a reserva do valor para que seja pago assim que o serviço prestado seja concluído e/ou o produto seja entregue ao poder público.
                  </div>
              
                  <svg slot="reference" class=" w-4 h-4 inline-block"
                  fill="none"
                  stroke="#333"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  ></path>
                </svg>
                </popper>
              </span>
            </div>
            <span :class="['c-despesa-main__category-icon', 'fill-status-'+category]" v-html="$assets.moedas" />
            <div v-if="values[category] !== undefined" class="c-despesa-main__category-value text-neutral-base uppercase font-bold mt-4 text-lg">R$ {{ formatCur(values[category]) }}</div>
          </div>
          <svg :class="i === 2 ? 'hidden' : 'block'" class="w-6 h-6 mx-5 fill-neutral-base" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
        </div>
    </div>

    <div v-if="this.pointInfo && updateTime" class="row mb-10">
        <div class="col-sm-12 c-despesa-main__category-info-date text-xs text-right text-neutral-light">
            {{ $t('data updated at') }}: {{ updateTime }}
        </div>
    </div>
  </div>
    </div>
    
</template>

<script>
import { mapState } from 'vuex'
import { formatCur } from '@/utils'
import Popper from 'vue-popperjs';
import 'vue-popperjs/dist/vue-popper.css';

export default {
  name: 'despesa-main',
  components: {
    'popper': Popper
  },
  data () {
    return {
      categories: ['planejado', 'empenhado', 'liquidado']
    }
  },
  computed: {
    values () {
      var values = {}
      
      values.planejado = this.pointInfo.sld_orcado_ano ? this.pointInfo.sld_orcado_ano : this.pointInfo.vl_orcado_ano
      if (this.pointInfo.vl_atualizado) values.planejado = this.pointInfo.vl_atualizado
      values.empenhado = this.pointInfo.vl_empenhadoliquido
      values.liquidado = this.pointInfo.vl_liquidado
      console.log(values.planejado)
      return values
    },
    updateTime () {
      if (this.pointInfo) {
        if (this.pointInfo.dataextracao) return this.pointInfo.dataextracao
        if (this.pointInfo.datafinal) return this.pointInfo.datafinal
        if (this.pointInfo['cd_anoexecucao']) return this.pointInfo['cd_anoexecucao']
        if (this.pointInfo['cd_exercicio']) return this.pointInfo['cd_exercicio']
      }
      return undefined
    },
    ...mapState({
      pointInfo: state => state.money.pointInfo
      // empenhos: state => state.empenhos.empenhos
    })
  },
  methods: {
    formatCur
  }
}
</script>

<style lang="scss">
  .c-despesa-main{
    &__category {
      &-icon {
        svg {
          width: 8rem;
        }
      }
    }
  }
</style>