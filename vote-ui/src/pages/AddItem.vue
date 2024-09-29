<template>
  <div>
    <h1>Add Item Page</h1>
    <NewItemForm />
  </div>
</template>

<script lang="ts">
import NewItemForm from '../components/NewItemForm.vue';

export default {
  name: 'additem',
  components: {
    NewItemForm,
  },
};
</script>
