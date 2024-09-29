<template>
  <div>
    <nav>
      <a href="#" @click.prevent>
        <img src="./assets/logo.png" class="logo" />
      </a>
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/additem">Add Item</router-link></li>
        <li><router-link to="/allitems">AllItems</router-link></li>
        <li><router-link to="/votes">Votes</router-link></li>
      </ul>
    </nav>

    <router-view />
  </div>
</template>

<script lang="ts">
export default {
  name: 'App',
}
</script>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

nav ul {
  list-style-type: none;
  display: flex;
  gap: 10px;
}
</style>
