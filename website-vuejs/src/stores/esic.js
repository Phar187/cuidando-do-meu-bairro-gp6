import Vue from 'vue'
import Vapi from 'vuex-rest-api'
import { baseUrls } from '@/configs'
import { http, addToStore } from '@/utils'

const baseURL = baseUrls.esic

// EsicLivre
export default addToStore(new Vapi({
  axios: http,
  baseURL,
  state: {
    orgaos: [],
    updates: [],
    pedidos: [],
    prepedidos: [],
    userPerguntas: [],
    stats: {}
  }
}).get({
  action: 'getPedidos',
  path: ({ key }) => `/keywords/${key}`,
  onSuccess (state, payload, axios) {
    function pedidosCompare (a, b) {
      let aDate = 0
      let bDate = 0
      if (a.history.length) aDate = a.history[0].date
      else aDate = a.request_date
      if (b.history.length) bDate = b.history[0].date
      else bDate = b.request_date
      return aDate < bDate ? 1 : -1
    }
    // Substitute strings for Dates
    for (let pedido of payload.data.pedidos) {
      if (pedido.request_date) pedido.request_date = new Date(pedido.request_date)
      for (let message of pedido.history) {
        message.date = new Date(message.date)
      }
    }
    state.pedidos = payload.data.pedidos.sort(pedidosCompare)
    state.prepedidos = payload.data.prepedidos || []
  }
}).get({
  action: 'getOrgaos',
  property: 'orgaos',
  path: `/orgaos`,
  onSuccess: (state, payload, axios) => {
    state.orgaos = payload.data.orgaos.sort().map((x) => { return { key: x, value: x } })
  }
}).get({
  action: 'getEsicStats',
  property: 'stats',
  path: ({ grouping }) => `/stats/${grouping}`
}).get({
  action: 'getUserPerguntas',
  property: 'userPerguntas',
  path: ({ username }) => `/authors/${username}`,
  onSuccess: (state, payload, axios) => {
    state.userPerguntas = payload.data.pedidos.reverse()
  }
}).get({
  action: 'getPedidosUpdates',
  property: 'updates',
  path: `/messages`,
  onSuccess: (state, payload, axios) => {
    // Substitute strings for Dates
    let pedidos = []
    for (let row of payload.data.messages) {
      row.date = new Date(row.date)
      if (row.keywords[0] !== 'recuperado') {
        pedidos.push({
          date: row.date,
          code: row.keywords[0],
          pedido: row
        })
      }
    }
    state.updates = pedidos
  }
}).getStore(),
{
  mutations: {
    sendingPergunta (state) {
      Vue.set(state.pending, 'sendingPergunta', true)
    },
    sentPergunta (state) {
      Vue.set(state.pending, 'sendingPergunta', false)
    }
  },
  actions: {
    async updatePedidos ({ rootState, dispatch, commit }) {
      // TODO needed to bypass cache. improve?
      let key = rootState.route.params.code
      let url = `${baseURL}/keywords/${key}`
      await http.get(url, { forceUpdate: true })
      return dispatch('getPedidos', { params: { key } })
    },
    async sendPergunta ({ dispatch, commit }, { keywords, orgao, text }) {
      let url = `${baseURL}/pedidos`
      let data = {
        token: await dispatch('getMicroToken'),
        text,
        orgao,
        keywords
      }
      commit('sendingPergunta')
      try {
        await http.post(url, data)
        dispatch('addSuccess', 'Question sent')
      } catch (err) {
        dispatch('addError', 'error_send_question')
      }
      commit('sentPergunta')

      dispatch('updatePedidos')
    },
    async sendRecurso ({ dispatch, commit }, { protocolo, text }) {
      let url = `${baseURL}/recurso/{protocolo}`
      let data = {
        token: await dispatch('getMicroToken'),
        text
      }
      commit('sendingPergunta')
      try {
        await http.post(url, data)
        dispatch('addSuccess', 'Appeal sent')
      } catch (err) {
        dispatch('addError', 'error_send_question')
      }
      commit('sentPergunta')

      dispatch('updatePedidos')
    }
  }
})
