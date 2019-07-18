import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    pen: false,
    filename: '',
    realName: '',
    text: '',
    tags: ''
  },
  getters: {
    getPen (state) {
      return state.pen
    },
    getFilename (state) {
      return state.filename
    },
    getRealName (state) {
      return state.realName
    },
    getText (state) {
      return state.text
    },
    getTags (state) {
      return state.tags
    }
  },
  mutations: {
    setPen (state) {
      state.pen = true
    },
    unsetPen (state) {
      state.pen = false
    },
    setFilename (state, filename) {
      state.filename = filename
    },
    setText (state, text) {
      state.text = text
    },
    setTags (state, tags) {
      state.tags = tags
    },
    setRealName (state, realName) {
      state.realName = realName
    }
  }
})

export default store
