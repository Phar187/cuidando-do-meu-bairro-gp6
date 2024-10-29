<template>
    <div v-if="yearInfo" class="row charts">
        <div class="col-lg-6 margin-bottom">
            <div class="inline-block donut-group not-mapped">
                <labeled-doughnut :color="$assets.patNM" :percentage="perNotMapped"/>
                <p class="text-secondary-base font-bold text-xl">{{rowsNotMapped}}</p>
                <p class="text-secondary-base font-bold text-sm">{{ $t('Not mapped') }}</p>
            </div>
            <div class="inline-block donut-group mapped">
                <labeled-doughnut :color="$assets.patM" :percentage="perMapped"/>
                <p class="text-primary-base font-bold text-xl">{{rowsMapped}}</p>
                <p class="text-primary-base font-bold text-sm">{{ $t('Mapped') }}</p>
            </div>
        </div>

        <div class="col-lg-6 mt-10 hidden">
            <div class="inline-block values-block">
                <div v-for="(v, i) of values" :key="i" class="value-block flex justify-center items-center py-5 border-b border-gray-200">
                    <div class="icon-block text-center ">
                        <img :src="$assets[v.name]" class="w-5">
                        <span class="capitalize text-center text-neutral-base">{{ $t(v.name) }}</span>
                    </div>
                    <div class="bar-block inline-block">
                        <hor-bar :color="$assets.patNM"
                              extraclass="not-mapped"
                              :title="$t('Not mapped')"
                              :absolute="v.notMapped.abs"
                              :percentage="v.notMapped.per"/>
                        <hor-bar :color="$assets.patM"
                              extraclass="mapped"
                              :title="$t('Mapped')"
                              :absolute="v.mapped.abs"
                              :percentage="v.mapped.per"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex'
import { format } from '@/utils'
import HorBar from '@/components/chart/HorBar.vue'
import LabeledDoughnut from '@/components/chart/LabeledDoughnut.vue'

export default {
  name: 'year-charts',
  components: {
    HorBar,
    LabeledDoughnut
  },
  // mounted () {
  //   this.getYearInfo({ params: { year: this.year } })
  // },
  computed: {
    perMapped () {
      return Math.round(this.yearInfo.rows.mapped / this.yearInfo.rows.total * 100)
    },
    perNotMapped () {
      return 100 - this.perMapped
    },
    rowsNotMapped () {
      return format(this.yearInfo.rows.total - this.yearInfo.rows.mapped)
    },
    rowsMapped () {
      return format(this.yearInfo.rows.mapped)
    },
    values () {
      let values = []
      for (let info of this.yearInfo.values) {
        if (info.name !== 'orcado') {
          let notMapped = info.total - info.mapped
          values.push({
            name: info.name === 'atualizado' ? 'planejado' : info.name,
            mapped: {
              abs: `R$${format(info.mapped)}`,
              per: Math.round(info.mapped / info.total * 100)
            },
            notMapped: {
              abs: `R$${format(notMapped)}`,
              per: Math.round(notMapped / info.total * 100)
            }
          })
        }
      }
      return values
    },
    ...mapState({
      yearInfo: state => state.money.yearInfo,
      year: state => state.route.params.year
    })
  }
}
</script>

<style lang="scss">
  .canvas-wrapper {
    display: table;
    font-size: 20pt;
    height: 200px;
    width: 200px;
  }
  canvas.donut {
    position: absolute;
  }
  .canvas-text {
    display: table-cell;
    text-align: center;
    vertical-align: middle;
    font-size: 20pt;
    color: #6c6c6c;
  }
  .donut-group {
    font-weight: 700;
    width: 200px;
  }
</style>