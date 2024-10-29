import Vue from 'vue'
import i18n from '@/i18n'
import VueApexCharts from 'vue-apexcharts'
import { sync } from 'vuex-router-sync'
import App from '@/App.vue'
import router from '@/router'
import store from '@/stores'
import Assets from '@/assets'
import ModalBox from '@/components/ModalBox'
import ButtonSpinner from '@/components/ButtonSpinner'
import StyledSelect from '@/components/StyledSelect.vue'
import SpinnerAnim from '@/components/SpinnerAnim'
import LazyTube from "vue-lazytube"

import 'leaflet/dist/leaflet.css'
import 'leaflet.markercluster/dist/MarkerCluster.css'

import '@/assets/styles/fonts.css'
import "@/assets/styles/tailwind.css"

import L from 'leaflet'
import 'flowbite'
import './assets/tailwind.css'

import '@/assets/styles/main.css'


delete L.Icon.Default.prototype._getIconUrl

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
})

Vue.config.productionTip = false

Vue.use(Assets)
Vue.use(VueApexCharts)
Vue.use(LazyTube);
Vue.component('modal-box', ModalBox)
Vue.component('button-spinner', ButtonSpinner)
Vue.component('styled-select', StyledSelect)
Vue.component('spinner-anim', SpinnerAnim)
Vue.component("LazyTube", LazyTube)


// Allows calling function when clicked outside of an element
// Usefull for modal and styled select
Vue.directive('click-outside', {
  bind: function (el, binding, vnode) {
    el.clickOutsideEvent = function (event) {
      if (!(el === event.target || el.contains(event.target))) {
        vnode.context[binding.expression](event)
      }
    }
    document.body.addEventListener('click', el.clickOutsideEvent)
  },
  unbind: function (el) {
    document.body.removeEventListener('click', el.clickOutsideEvent)
  }
})

sync(store, router)

new Vue({
  router,
  store,
  i18n,
  render: h => h(App)
}).$mount('#app')
