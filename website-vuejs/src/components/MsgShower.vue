<template>
  <transition-group tag="div" name="fade">
    <div v-for="msg in msgs" :key="msg.id" id="toast-bottom-right" class="fixed flex items-center w-full max-w-xs p-4 space-x-4 bg-white divide-x divide-gray-200 rounded-lg shadow left-5 bottom-5" role="alert">
      <div class="text-sm font-normal text-red-800">{{ $t(msg.text) }}</div>
      <button type="button" @click="removeMsg(msg)" class="ml-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8" aria-label="Close">
            <span class="sr-only">Close</span>
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
       </button>
    </div>
  </transition-group>
</template>

<script>
import { mapState, mapMutations } from 'vuex'
export default {
  name: 'msg-shower',
  computed: mapState({
    msgs: state => state.msgs.msgs
  }),
  methods: mapMutations(['removeMsg'])
}
</script>
