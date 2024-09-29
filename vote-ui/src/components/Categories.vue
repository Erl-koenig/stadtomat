<script setup lang="ts">
import { onMounted, ref } from 'vue';
import supabase from '../services/supabase.ts';

interface Category {
  id: string
  title: string
  description: string
  created_at: string
}

const categories = ref<Category[]>([]);

async function getCategories() {
  let { data, error } = await supabase
    .from('category')
    .select('*')
  if (error) {
    console.log(error);
  } else {
    categories.value = data as Category[];
  }
}

onMounted(() => {
  getCategories();
});
</script>

<template>
  <div>
    <h2>Categories</h2>
    <button type="button" @click="getCategories">Refresh</button>
    <ul>
      <li v-for="category in categories" :key="category.id">
        <b>{{ category.title }}:</b> {{ category.description }}
      </li>
    </ul>
  </div>
</template>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}
</style>
