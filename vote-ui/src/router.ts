import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

import Home from "./pages/Home.vue";
import AddItems from "./pages/AddItem.vue";
import AllItems from "./pages/AllItems.vue";
import Votes from "./pages/Votes.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/additem",
    name: "AddItems",
    component: AddItems,
  },
  {
    path: "/allitems",
    name: "AllItems",
    component: AllItems,
  },
  {
    path: "/votes",
    name: "Votes",
    component: Votes,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
