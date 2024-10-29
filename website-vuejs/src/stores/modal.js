export default {
  state: {
    current: null
  },
  mutations: {
    openModal (state, id) {
      state.current = id
    },
    closeModal (state) {
      state.current = null
    }
  }
}
