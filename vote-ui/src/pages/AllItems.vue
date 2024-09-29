<template>
  <div>
    <h1>All items Page</h1>
    <ListItems />
  </div>
</template>

<script lang="ts">
import ListItems from '../components/ListItems.vue';

export default {
  name: 'allitems',
  components: {
    ListItems,
  },
};
</script>
