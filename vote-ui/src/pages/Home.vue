<template>
  <div>
    <h1>Home Page</h1>
    <Categories />
  </div>
</template>

<script lang="ts">
import Categories from '../components/Categories.vue';

export default {
  name: 'Home',
  components: {
    Categories,
  },
};
</script>

<style scoped></style>
