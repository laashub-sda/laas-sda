const routers = [
  {
    path: '/',
    meta: {
      title: 'Workstation'
    },
    component: (resolve) => require(['./service/Workstation.vue'], resolve)
  },
  {
    path: '/designer/bdm',
    meta: {
      title: 'BDM-Designer'
    },
    component: (resolve) => require(['./service/designer/bdm/BDM.vue'], resolve)
  },
];
export default routers;
