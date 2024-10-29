<template>
  <div class="canvas-wrapper">
    <canvas ref="canvas" class="donut" :width="width" :height="height"/>
    <span class="darker-text canvas-text">{{ percentage }}%</span>
  </div>
</template>

<script>
import { drawDonut } from './chart-utils'
export default {
  name: 'labeled-doughnut',
  props: {
    percentage: Number,
    color: String
  },
  mounted () {
    drawDonut(this.$refs.canvas, this.color, this.percentage)
  },
  watch: {
    percentage (newValue, oldValue) {
      drawDonut(this.$refs.canvas, this.color, newValue)
    }
  },
  data () {
    return {
      width: 200,
      height: 200
    }
  }
}
</script>
