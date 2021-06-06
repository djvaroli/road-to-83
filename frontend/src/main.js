import Vue from 'vue'
import App from './App.vue'

import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import VueApexCharts from 'vue-apexcharts'

import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(Buefy)
Vue.use(VueApexCharts)
Vue.use(VueAxios, axios)
Vue.axios.defaults.baseURL = process.env.VUE_APP_BASE_URL


Vue.component('apexchart', VueApexCharts)
Vue.config.productionTip = false


new Vue({
  render: h => h(App),
}).$mount('#app')
