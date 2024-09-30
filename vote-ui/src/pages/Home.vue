<script lang="ts">
import Button from '@/components/ui/button/Button.vue';
import Categories from '../components/Categories.vue';


export default {
  name: 'Home',
  components: {
    Categories,
  },
};
</script>

<template>
  <div>
    <h1>Home Page</h1>

    <Button>Button</Button>

    <Categories />
  </div>
</template>

<style scoped></style>
