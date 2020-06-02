const routers = [
  // service
  {
    path: '/',
    meta: {
      title: 'Workstation'
    },
    component: (resolve) => require(['./service/Workstation.vue'], resolve)
  },
  {
    path: '/designer',
    meta: {
      title: 'Designer'
    },
    component: (resolve) => require(['./service/designer/Designer'], resolve)
  },
  {
    path: '/dashboard',
    meta: {
      title: 'Dashboard'
    },
    component: (resolve) => require(['./service/dashboard/Dashboard'], resolve)
  },
];
export default routers;
