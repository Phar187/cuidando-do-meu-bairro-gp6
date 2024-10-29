<template>
  <div class="outer-bar">
    <div class="inner-bar"
        @mouseenter="isShowingTooltip = true"
        @mouseleave="isShowingTooltip = false"
        :style="style"/>
    <div role="tooltip" v-if="isShowingTooltip" :class="[extraclass]"  class="inline-block absolute z-10 py-2 px-3 text-sm font-medium text-white bg-gray-900 rounded-lg shadow-sm opacity-0 transition-opacity duration-300 tooltip">
        {{ absolute }} {{ title }}
        <div class="tooltip-arrow" data-popper-arrow></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'hor-bar',
  props: {
    percentage: Number,
    color: String,
    'extraclass': String,
    absolute: [String, Number],
    title: String
  },
  computed: {
    style () {
      return { width: this.percentage + '%', 'background-image': `url(${this.color})` }
    }
  },
  data () {
    return {
      isShowingTooltip: false
    }
  }
}
</script>

<style lang="scss" scoped>
  .outer-bar {
    height: 20px;
    margin: 2px 10px;
    position: relative;
    width: 360px;
  }
  .inner-bar {
    border-radius: 3px;
    height: 100%;
  }
</style>