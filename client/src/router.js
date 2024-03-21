import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue';
import RegisterView from './views/RegisterView.vue';
import LoginView from './views/LoginView.vue';
import DashboardView from './views/DashboardView.vue';
import ProfileView from './views/ProfileView.vue';
import MailingsView from "./views/MailingsView.vue";
import ScheduledMailingsView from "./views/ScheduledMailingsView.vue";
import TemplatesView from "./views/TemplatesView.vue";
import NotFound from "./views/NotFound.vue";
import MailingManageView from './views/MailingManageView.vue';

import { useAuthStore } from "./components/store/userAuth.js";

const routes = [
  {
    path: '/',
    name: "Home",
    component: HomeView,
  },
  {
    path: '/register',
    name: 'Registration',
    component: RegisterView,
    beforeEnter: authGuardForLoginAndRegister,
  },
  {
    path: '/login',
    name: 'Authorization',
    component: LoginView,
    beforeEnter: authGuardForLoginAndRegister,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    beforeEnter: authGuard,
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView,
    beforeEnter: authGuard,
  },
  {
    path: '/mailings',
    name: 'Mailings',
    component: MailingsView,
    beforeEnter: authGuard,
  },
  {
    path: '/templates',
    name: 'Templates',
    component: TemplatesView,
    beforeEnter: authGuard,
  },
  {
    path: '/scheduledMailings',
    name: 'ScheduledMailings',
    component: ScheduledMailingsView,
    beforeEnter: authGuard,
  },
  {
    path: '/mailings/mailingManage/:mailingId',
    name: 'MailingManage',
    component: MailingManageView,
    beforeEnter: (to, from, next) => {
      // Проверяем значение параметра маршрута
      if (to.params.mailingId === '-1' || to.params.mailingId === 'create') {
        // Если параметр равен "-1" или "create", переходим на создание рассылки
        next();
      } else {
        // В противном случае, продолжаем нормальную навигацию
        next();
      }
    },
  },
  

  { path: "/:notFound(.*)", component: NotFound },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

function authGuard(to, from, next) {
  const authStore = useAuthStore();
  if (authStore.isAuthenticated) {
    next();
  } else {
    next({ name: "Authorization" });
  }
}

function authGuardForLoginAndRegister(to, from, next) {
  const authStore = useAuthStore();
  if (!authStore.isAuthenticated) {
    next();
  } else {
    next({ name: "Home" });
  }
}

export default router