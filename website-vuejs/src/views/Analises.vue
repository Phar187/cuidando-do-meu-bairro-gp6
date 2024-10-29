<template>
  <div class="pg-analisys">
    <div class="container mx-auto my-20 h-full">
      <h1 class="pg-analisys__title text-neutral-base text-4xl font-bold">
        Perguntas feitas por {{ $t(grouping) }}
      </h1>
      <div class="pg-analisys__control-buttons mt-4 mb-2">
        <span class="text-neutral-base">Selecione por:</span>
        <button v-for="g of Object.keys(groupConfig)" :key="g"
                class="pg-analisys__control-buttons-btn px-3 py-1 bg-secondary-light text-white rounded ml-2 hover:bg-secondary-base disabled:bg-secondary-base"
                :disabled="grouping === g"
                @click="getData(g)">
          {{ $t(g) }}
        </button>
      </div>
      <apexcharts v-if="esicStats.dates" height="400" type="line" :options="chartOptions" :series="series"></apexcharts>

      <h2 class="pg-analisys__subtitle text-neutral-base text-3xl font-bold mt-6 mb-3">Perguntas feitas por órgão</h2>     
      <div class="pg-analisys__table table-responsive">
        <div class="flex flex-col">
          <div class="overflow-x-auto sm:-mx-6 lg:-mx-8">
            <div class="py-2 inline-block min-w-full sm:px-6 lg:px-8">
              <div class="overflow-hidden">
                <table class="min-w-full">
                  <thead class="bg-white border-b">
                    <tr>
                      <th scope="col" class="text-sm font-medium text-neutral-base px-6 py-4 text-left">
                        Órgão
                      </th>
                      <th scope="col" class="text-sm font-medium text-neutral-base px-6 py-4 text-left">
                        Número de Pedidos
                      </th> 
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="row of esicStats.orgaos" :key="row.name" class="bg-white border-b transition duration-300 ease-in-out hover:bg-gray-100">
                     <td class="text-sm text-neutral-base font-light px-6 py-4 whitespace-nowrap">{{ row.name }}</td>
                      <td class="text-sm text-neutral-base font-light px-6 py-4 whitespace-nowrap">{{ row.count }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'
import { mapActions, mapState } from 'vuex'
import FooterInfo from '../components/FooterInfo.vue'

export default {
  components: {
    apexcharts: VueApexCharts,
    FooterInfo
  },
  data () {
    return {
      grouping: 'year',
      groupConfig: {
        'day': {
          tooltipFormat: 'dd MMM yyyy',
          datetimeFormatter: {
            year: 'dd MMM yyyy',
            month: 'dd MMM yyyy',
            day: 'dd MMM yyyy',
            hour: ''
          }
        },
        'month': {
          tooltipFormat: 'MMM yyyy',
          datetimeFormatter: {
            year: 'MMM yyyy',
            month: 'MMM yyyy',
            day: '',
            hour: ''
          }
        },
        'year': {
          tooltipFormat: 'yyyy',
          datetimeFormatter: {
            year: 'yyyy',
            month: '',
            day: '',
            hour: ''
          }
        }
      }
    }
  },
  computed: {
    ...mapState({
      esicStats: state => state.esic.stats
    }),
    series () {
      return [{
        name: 'perguntas',
        // data: this.esicStats.dates.map(x => x[1])
        data: this.esicStats.dates
      }]
    },
    chartOptions () {
      return {
        chart: {
          // id: 'vuechart-example'
          locales: [
            {
              'name': 'pt',
              'options': {
                'months': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
                'shortMonths': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
                'days': ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'],
                'shortDays': ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab'],
                'toolbar': {
                  'download': 'Baixar SVG',
                  'selection': 'Selecionar',
                  'selectionZoom': 'Selecionar Zoom',
                  'zoomIn': 'Aumentar',
                  'zoomOut': 'Diminuir',
                  'pan': 'Navegação',
                  'reset': 'Reiniciar Zoom'
                }
              }
            }
          ],
          defaultLocale: 'pt'
        },
        xaxis: {
          type: 'datetime',
          // tickAmount: 6,
          // labels: {
          //   formatter: function (val, timestamp) {
          //     return val
          //   }
          // }
          // categories: this.esicStats.dates.map(x => x[0]),
          labels: {
            datetimeFormatter: this.groupConfig[this.grouping].datetimeFormatter
          },
          tooltip: {
            enabled: false
          }
        },
        markers: {
          size: 0,
          style: 'hollow'
        },
        grid: {
          row: {
            colors: ['#f3f3f3', 'transparent'],
            opacity: 0.5
          }
        },
        tooltip: {
          x: {
            format: this.groupConfig[this.grouping].tooltipFormat
          }
        }
      }
    }
  },
  methods: {
    ...mapActions([
      'getEsicStats'
    ]),
    getData (grouping) {
      if (grouping) this.grouping = grouping
      this.getEsicStats({ params: { grouping: this.grouping } })
    }
  },
  mounted () {
    this.getData()
  }
}
</script>
