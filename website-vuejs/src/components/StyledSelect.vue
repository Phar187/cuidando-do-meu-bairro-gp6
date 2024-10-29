<template>
  <div class="w-full">
    <button 
      class="text-neutral-base bg-transparent border border-neutral-base font-medium rounded text-sm px-4 py-4 text-center inline-flex items-center justify-between w-full"
      type="button"
      data-dropdown-toggle="dropdownYear"
      v-click-outside="close"
      @click="toggleList"
      :aria-expanded="open"
    >
      {{ displayedValue }}
      <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
      </svg>
    </button>

    <div v-if="open" class="scroll-year-select absolute z-10 h-52 overflow-scroll scroll-smooth bg-white divide-y divide-gray-100 rounded shadow">
      <ul class="py-1 text-sm text-gray-700">
        <li 
          v-for="option of options"
          :key="option.key"
          :data-key="option.key"
          @click="optionSelected"
          role="option"
          class="block px-4 py-2 hover:bg-gray-100"
        >
          {{ option.value }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'styled-select',
  props: {
    options: Array,
    // Used to bind the displayed selected value
    // If not passed, use a variable internal to this component (internalSelectedValue)
    value: [String, Number]
  },
  data () {
    return {
      open: false,
      internalSelectedValue: null
    }
  },
  computed: {
    displayedValue () {
      let key = this.value ? this.value : this.internalSelectedValue
      for (let option of this.options) {
        if (option.key === key) return option.value
      }
      return '...'
    }
  },
  methods: {
    toggleList () {
      this.open = !this.open
    },
    close () {
      this.open = false
    },
    optionSelected (event) {
      this.internalSelectedValue = event.target.dataset.key
      this.open = false
      this.$emit('input', this.internalSelectedValue)
    }
  }
}
</script>
