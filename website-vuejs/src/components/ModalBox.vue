<template>
  <transition name="fade">
    <div v-if="openModal">
      <div class="modal-backdrop bg-black opacity-70 z-1 top-0 bottom-0 left-0 right-0 fixed"/>
      <div
        class="modal z-1000 bottom-0 left-0 right-0 fixed w-full md:inset-0 md:top-8 h-modal md:h-full"
        tabindex="-1"
        role="dialog"
        aria-labelledby="myModalLabel"
        style="display:block;"
      >
        <div
          id="modal-dialog"
          class="modal-dialog relative p-4 w-full max-w-2xl h-full md:h-auto"
          role="document"
        >
          <div class="modal-content relative bg-white rounded-lg shadow">
            <div class="flex justify-between items-center p-2 bg-primary-base rounded-t-lg">
                <div class="modal-header px-5">
                    <img class="block-center w-44" :src="$assets.logo">
                </div>
                <div>
                  <button type="button" aria-label="Close" class="bg-secondary-light text-white bg-transparent hover:bg-secondary-base rounded-lg text-sm p-1.5 ml-auto inline-flex items-center" @click="closeModal">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>  
                  </button>
                </div>
            </div>
            <slot/>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { mapState, mapMutations } from 'vuex'

export default {
  name: 'modal-box',
  props: {
    modalId: String
  },
  computed: {
    ...mapState({
      openModal (state) { return state.modal.current === this.modalId }
    })
  },
  methods: {
    ...mapMutations(['closeModal'])
  }
}
</script>

<style lang="scss" scoped>
  .modal {
    overflow-x: hidden;
    overflow-y: auto;
  }
  .modal-dialog {
    margin: 30px auto;
  }
</style>
