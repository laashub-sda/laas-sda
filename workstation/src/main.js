import Vue from 'vue'
import VueRouter from 'vue-router';
import App from './App.vue';
import routers from './router'
import ViewUI from 'view-design';
import 'view-design/dist/styles/iview.css';
import VueCodemirror from 'vue-codemirror'
import 'codemirror/lib/codemirror.css'

import init from './init'

Vue.use(VueRouter);
Vue.use(ViewUI);
Vue.use(VueCodemirror);

Vue.config.productionTip = false;

const router = new VueRouter({
  mode: 'history',
  routes: routers
});

init.init();

new Vue({
  el: '#app',
  router: router,
  render: h => h(App)
});
