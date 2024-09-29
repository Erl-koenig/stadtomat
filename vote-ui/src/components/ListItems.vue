<template>
  <div>
    <h2>Items List</h2>
    <table>
      <thead>
        <tr>
          <th>Title</th>
          <th>Description</th>
          <th>Category</th>
          <th>Tag</th>
          <th>Image</th>
          <th>Created At</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td>{{ item.title }}</td>
          <td>{{ item.description }}</td>
          <td>{{ item.category }}</td>
          <td>{{ item.tag }}</td>
          <td>
            <img v-if="item.image" :src="item.image" alt="Item Image" class="item-image" />
          </td>
          <td>{{ formatDate(item.created_at) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import supabase from '../services/supabase.ts';

export default defineComponent({
  name: 'ListItems',
  setup() {
    const items = ref([]);

    const fetchItems = async () => {
      const { data, error } = await supabase
        .from('piece')
        .select('id, title, description, category, tag, image, created_at');

      console.log(data);
      if (error) {
        console.error('Error fetching items:', error);
      } else {
        // Construct the full image URL
        items.value = data.map(item => {
          return {
            ...item,
            image: item.image ? `https://lzirjhubrvqfumpsmenv.supabase.co/storage/v1/object/public/piece_image/${item.image}` : null
          };
          console.log(item);
        });
      }
    };


    const formatDate = (dateString: string) => {
      const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    };

    onMounted(fetchItems);

    return { items, formatDate };
  },
});
</script>

<style scoped>
.item-image {
  max-width: 100px;
  height: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
</style>
