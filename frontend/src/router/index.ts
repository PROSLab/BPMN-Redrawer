import { Notify } from 'quasar';
import { route } from 'quasar/wrappers';
import { i18n } from 'src/boot/i18n';
import { useBpmnStore } from 'src/store/bpmnStore';
import {
  createMemoryHistory,
  createRouter,
  createWebHashHistory,
  createWebHistory,
} from 'vue-router';
import routes from './routes';

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === 'history'
    ? createWebHistory
    : createWebHashHistory;

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(
      process.env.MODE === 'ssr' ? void 0 : process.env.VUE_ROUTER_BASE
    ),
  });

  Router.beforeEach((to, _from, next) => {
    if (to.meta.auth) {
      // If we are about to visit a page that needs authentication
      // (e.g. history page), check that the user is logged in
      const bpmnStore = useBpmnStore();
      if (bpmnStore.logged) {
        // If the user is logged in, visit the page
        next();
      } else {
        // Otherwise notify the user about the error and
        // redirect him to the home page
        Notify.create({
          message: i18n.global.t('router.noAuth'),
          type: 'negative',
        });
        next({ name: 'home' });
      }
    } else {
      // Visit the page without any checks if the route doesn't need them
      next();
    }
  });

  return Router;
});
