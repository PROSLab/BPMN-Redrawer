import { boot } from 'quasar/wrappers';
import axios, { AxiosInstance } from 'axios';
import { useBpmnStore } from 'src/store/bpmnStore';
import { auth } from 'src/components/utils/firebase-utils';

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
  }
}

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const api = axios.create({
  baseURL: 'http://localhost:5000/api/v1',
});

// Intercept requests to backend API and add Firebase token
// to the headers if user is logged in
api.interceptors.request.use(
  async (config) => {
    const bpmnStore = useBpmnStore();
    if (bpmnStore.logged) {
      const token = await auth.currentUser?.getIdToken();
      (config.headers as { Authorization: string })[
        'Authorization'
      ] = `Bearer ${token as string}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});

export { api };
