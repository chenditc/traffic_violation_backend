import { defineConfig } from 'umi';

export default defineConfig({
  nodeModulesTransform: {
    type: 'none',
  },
  routes: [
    { path: '/', redirect: "/login" },
    { path: "/login", component: "@/pages/Login.tsx"},
    { path: '/list', component: "@/pages/EventList.tsx"},
    { path: '/report', component: "@/pages/Report.tsx"}
  ],
  fastRefresh: {},
  styles: ["#root {height: 100%}"],
  antd: { mobile: false }
});
