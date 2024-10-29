import Vue from 'vue'
import { baseUrls } from '@/configs'
import { http } from '@/utils'

const baseURL = baseUrls.subscriptions

export default {
  state: {
    subscriptions: {},
    pending: {
      subscribe: {},
      unsubscribe: {}
    }
  },
  mutations: {
    changePending (state, { type, id, value }) {
      Vue.set(state.pending[type], id, value)
    },
    setUserSubscriptions (state, { subscriptions }) {
      state.subscriptions = subscriptions
    }
  },
  actions: {
    async getSubscriptions ({ rootState, commit }) {
      let url = `${baseURL}/subscriptions`
      let data = {
        // subscriber: rootState.route.params.viewingUser
        subscriber: rootState.auth.username
      }
      let response = await http.post(url, data)
      let subscriptions = {}
      for (let s of response.data.subscriptions) {
        subscriptions[s.tag] = s
      }
      return commit('setUserSubscriptions', { subscriptions })
    },
    async subscribe ({ rootState, commit, dispatch }, { author, tag }) {
      let url = `${baseURL}/subscriptions`
      let data = {
        token: await dispatch('getMicroToken'),
        subscriptions: [{
          tag,
          author,
          template_data: { link: window.location.href }
        }]
      }
      commit('changePending', { type: 'subscribe', id: tag, value: true })
      await http.put(url, data)
      commit('changePending', { type: 'subscribe', id: tag, value: false })
      dispatch('getSubscriptions')
    },
    async unsubscribe ({ dispatch, commit }, { tag }) {
      let url = `${baseURL}/subscriptions`
      let data = {
        token: await dispatch('getMicroToken'),
        tags: [tag]
      }
      commit('changePending', { type: 'unsubscribe', id: tag, value: true })
      await http.delete(url, { data })
      commit('changePending', { type: 'unsubscribe', id: tag, value: false })
      dispatch('getSubscriptions')
    }
  }
}
