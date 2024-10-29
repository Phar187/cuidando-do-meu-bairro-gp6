<template>
  <button class="btn btn-color-sec inline-block" :disabled="condition || disabled">
    <spinner-anim v-if="condition"/>
    <span :class="{ transparent: condition }">
      <slot/>
    </span>
    
  </button>
</template>

<script>
export default {
  name: 'button-spinner',
  props: {
    condition: Boolean,
    disabled: {
      type: Boolean,
      default: false
    }
  }
}
</script>
