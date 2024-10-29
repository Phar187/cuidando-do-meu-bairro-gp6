<template>
  <Popper v-bind="$attrs" hover openDelay="200" closeDelay="100">
    <slot />
    <template #content="props">
      <slot name="content" v-bind="props" />
    </template>
  </Popper>
</template>

<script lang="ts">
import Popper from "vue-popperjs";

export default {
  name: "TooltipInfo",
  components: {
    'Popper': Popper,
  },
};
</script>

<style lang="postcss" scoped>
:deep(.popper) {
  width: 50%;
  background: #00667D;
  padding: 20px;
  border-radius: 20px;
  color: #ffffff;
  font-weight: bold;
}

:deep(.popper #arrow::before) {
  background: #00667D;
}
:deep(.popper:hover),
:deep(.popper:hover > #arrow::before) {
  background: #00667D;
}
</style>
