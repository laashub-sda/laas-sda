const routers = [
  // service
  {
    path: '/',
    meta: {
      title: 'BDM-Designer'
    },
    component: (resolve) => require(['./service/BDM-Designer.vue'], resolve)
  },
];
export default routers;
