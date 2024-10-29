export default {
  state: {
    msgs: [],
    lastId: 0
  },
  mutations: {
    // Add a message
    addMsg (state, msg) {
      msg.id = state.lastId
      state.lastId += 1
      state.msgs.push(msg)
    },
    // Remove a message
    removeMsg (state, msg) {
      let index = state.msgs.indexOf(msg)
      if (index !== -1) {
        state.msgs.splice(index, 1)
      }
    }
  },
  actions: {
    // Add a message by type
    addMsgType ({ commit }, { text, type }) {
      let msg = { text, type }
      commit('addMsg', msg)
      setTimeout(() => commit('removeMsg', msg), 5000)
    },
    // Add success message
    addSuccess ({ dispatch }, text) {
      dispatch('addMsgType', { text, type: 'success' })
    },
    // Add error message
    addError ({ dispatch }, text) {
      dispatch('addMsgType', { text, type: 'error' })
    }
  }
}
