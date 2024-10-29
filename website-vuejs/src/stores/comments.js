import Vue from 'vue'
import Vapi from 'vuex-rest-api'
import { baseUrls } from '@/configs'
import { http, addToStore } from '@/utils'

const baseURL = baseUrls.comments

// Comments
export default addToStore(new Vapi({
  axios: http,
  baseURL,
  state: {
    updates: [],
    commentsPage: [],
    pending: {
      edit: {},
      reply: {},
      voteup: {},
      delete: {},
      report: {},
      votedown: {}
    }
  }
}).get({
  action: 'getCommentsUpdates',
  property: 'updates',
  path: `/comment`,
  onSuccess (state, payload, axios) {
    // Substitute strings for Dates
    let updates = payload.data.comments
    for (let row of updates) {
      row.created = new Date(row.created)
      row.modified = new Date(row.modified)
    }

    let threads = []
    // TODO pegar infos sobre os pontos para mostrar os assuntos
    // falta só arrumar o triggerChange abaixo
    // Group comments by thread
    var threadsMap = updates.reduce((_threads, curr) => {
      if (_threads[curr.thread_name]) {
        _threads[curr.thread_name].push(curr)
      } else {
        let comments = [curr]
        _threads[curr.thread_name] = comments
        threads.push({
          date: curr.created,
          thread_name: curr.thread_name,
          comments
        })
      }
      return _threads
    }, {})

    // eslint-disable-next-line
    let codes = Object.keys(threadsMap)
    // this.triggerChange('multiPontinfo', {key: 'a', codes})

    state.updates = threads
  }
}).get({
  action: 'getComments',
  path: ({ key }) => `/thread/${key}`,
  onSuccess (state, payload) {
    function commentCompare (a, b) { return a.created < b.created ? 1 : -1 }
    function orderComments (comments) {
      // Substitute strings for Dates
      for (let comment of comments) {
        comment.created = new Date(comment.created)
        comment.modified = new Date(comment.modified)
      }
      comments.sort(commentCompare)
      for (let com of comments) {
        if (com.replies) orderComments(com.replies)
      }
      return comments
    }
    orderComments(payload.data.comments)
    state.commentsPage = payload.data
  }
}).getStore(),
{
  mutations: {
    setPending (state, { type, id }) {
      Vue.set(state.pending[type], id, true)
    },
    unsetPending (state, { type, id }) {
      Vue.set(state.pending[type], id, false)
    }
  },
  actions: {
    async updateThread ({ rootState, dispatch, commit }) {
      // TODO needed to bypass cache. improve?
      let thread = rootState.route.params.code
      let url = `${baseURL}/thread/${thread}`
      await http.get(url, { forceUpdate: true })
      return dispatch('getComments', { params: { key: thread } })
    },
    async sendComment ({ dispatch, commit }, { key, text }) {
      let url = `${baseURL}/thread/${key}`
      let data = {
        token: await dispatch('getMicroToken'),
        text
      }
      commit('setPending', { type: 'reply', id: key })
      await http.post(url, data)
      commit('unsetPending', { type: 'reply', id: key })

      dispatch('updateThread')
    },
    async sendDelete ({ dispatch, commit }, { url, id }) {
      url = baseURL + url
      let data = {
        token: await dispatch('getMicroToken')
      }
      commit('setPending', { type: 'delete', id })
      await http.delete(url, { data })
      commit('unsetPending', { type: 'delete', id })

      dispatch('updateThread')
    },
    async sendReport ({ dispatch, commit }, { url, id }) {
      url = baseURL + url
      commit('setPending', { type: 'report', id })
      await http.post(url)
      commit('unsetPending', { type: 'report', id })

      dispatch('updateThread')
    },
    async sendVote ({ dispatch, commit }, { url, id, vote }) {
      url = baseURL + url
      let data = {
        token: await dispatch('getMicroToken'),
        vote
      }
      commit('setPending', { type: 'vote', id })
      await http.post(url, data)
      commit('unsetPending', { type: 'vote', id })

      dispatch('updateThread')
    },
    async sendReply ({ dispatch, commit }, { url, id, text }) {
      url = baseURL + url
      let data = {
        token: await dispatch('getMicroToken'),
        text
      }
      commit('setPending', { type: 'reply', id })
      await http.post(url, data)
      commit('unsetPending', { type: 'reply', id })

      dispatch('updateThread')
    },
    async sendEdit ({ dispatch, commit }, { url, id, text }) {
      url = baseURL + url
      let data = {
        token: await dispatch('getMicroToken'),
        text
      }
      commit('setPending', { type: 'edit', id })
      await http.put(url, data)
      commit('unsetPending', { type: 'edit', id })

      dispatch('updateThread')
    }
  }
})
