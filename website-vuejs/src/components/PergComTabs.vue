<template>
  <div class="perg-com-tabs py-10">
    <div class="container light-dark-bg mx-auto">
      <div class="mb-4">
        <ul class="flex flex-wrap justify-around text-xl font-medium text-center text-neutral-base border-b border-gray-200">
          <li 
            class="tab w-1/2 cursor-pointer inline-block p-4 text-neutral-base hover:bg-gray-100 rounded-t-lg active" 
            :class="{ 'active border-b-4 border-primary-base dark:text-primary-base': tab.component === currTabComponent }"
            v-for="(tab, i) in tabs" :key="i"
            @click="currTabComponent = tab.component"
            role="tab"
            :aria-controls="tab.component"
          >
            <p class="capitalize">{{ counts[tab.component] }} {{ $t(tab.title) }}</p>
          </li>
        </ul>
      </div>
    </div>

    <div class="container mx-auto tabContent">
      <transition name="fade" mode="out-in">
        <component :is="currTabComponent"/>
      </transition>
    </div>
  </div>
</template>

<script>
import PerguntasTab from '@/components/perguntas/PerguntasTab.vue'
import CommentsTab from '@/components/comments/CommentsTab.vue'
import { mapState } from 'vuex'

export default {
  name: 'perg-com-tabs',
  components: {
    PerguntasTab,
    CommentsTab
  },
  data () {
    let tabs = [
      { title: 'questions', component: 'perguntas-tab', countArray: 'pedidos' },
      { title: 'comments', component: 'comments-tab', countArray: 'comments' }
    ]
    return {
      tabs,
      currTabComponent: tabs[0].component
    }
  },
  computed: {
    counts () {
      let counts = {}
      for (let tab of this.tabs) {
        counts[tab.component] = this[tab.countArray] ? this[tab.countArray].length : 0
      }
      return counts
    },
    ...mapState({
      pedidos: state => state.esic.pedidos,
      comments: state => state.comments.commentsPage.comments
    })
  }
}
</script>
