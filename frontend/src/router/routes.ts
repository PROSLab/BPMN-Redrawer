import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        redirect: '/home',
      },
      { path: 'home', name: 'home', component: () => import('pages/Home.vue') },
      {
        path: 'editor',
        name: 'editor',
        component: () => import('pages/Editor.vue'),
      },
      {
        path: 'history',
        name: 'history',
        component: () => import('pages/History.vue'),
        // metadata to let the router know this route needs authentication
        meta: { auth: true },
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue'),
  },
];

export default routes;
