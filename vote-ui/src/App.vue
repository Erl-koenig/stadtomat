<script setup lang="ts">
import { onMounted, ref } from 'vue';
import HelloWorld from './components/HelloWorld.vue'
import supabase from './services/supabase.ts'

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
    console.log(error)
  } else {
    categories.value = data as Category[]
  }
}

onMounted(() => {
  getCategories()
})
</script>

<template>
  <div>
    <a href="https://vitejs.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
  </div>
  <h2>Categories</h2>
  <button type="button" @click="getCategories">Refresh</button>
  <ul>
    <li v-for="category in categories" :key="category.id"><b>{{ category.title }}:</b> {{ category.description }}</li>
  </ul>
</template>

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

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
