import Vue from 'vue'
import Vuex from 'vuex'

import money from '@/stores/money'
import esic from '@/stores/esic'
import empenhos from '@/stores/empenhos'
import comments from '@/stores/comments'
import auth from '@/stores/auth'
import msgs from '@/stores/msgs'
import modal from '@/stores/modal'
import subscriptions from '@/stores/subscriptions'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    money,
    esic,
    empenhos,
    comments,
    auth,
    msgs,
    modal,
    subscriptions
  }
})
