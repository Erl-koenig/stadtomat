<template>
  <div id="app">
    <nav class="vertical-navbar">
      <a href="#" @click.prevent>
        <img src="./assets/logo.png" class="logo" />
      </a>
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/additem">Add Item</router-link></li>
        <li><router-link to="/allitems">All Items</router-link></li>
        <li><router-link to="/votes">Votes</router-link></li>
      </ul>
    </nav>
    <div class="content">
      <router-view />
    </div>
  </div>
</template>


<script setup lang="ts">
import { defineProps } from 'vue';
import { RouterView } from 'vue-router';

const props = defineProps<{
  msg: string;
}>();
</script>

<style scoped>
#app {
  display: flex;
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
}

.vertical-navbar {
  width: 200px;
  padding-right: 2rem;
  background-color: #1a1a1a;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
}

.vertical-navbar ul {
  list-style-type: none;
  padding: 0;
}

.vertical-navbar li {
  margin: 15px 0;
}

.content {
  margin-left: 220px;
  padding: 2rem;
  flex-grow: 1;
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

a {
  font-weight: 500;
  color: #646cff;
  text-decoration: inherit;
}

a:hover {
  color: #535bf2;
}
</style>
