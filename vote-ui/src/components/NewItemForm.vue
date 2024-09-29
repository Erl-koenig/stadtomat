<template>
  <div class="new-item-form">
    <h2>Add New Item</h2>
    <form @submit.prevent="handleSubmit">
      <div>
        <label for="title">Title:</label>
        <input type="text" id="title" v-model="title" required />
      </div>
      <div>
        <label for="description">Description:</label>
        <textarea id="description" v-model="description" required></textarea>
      </div>
      <div>
        <label for="image">Upload Image:</label>
        <input type="file" id="image" @change="handleImageUpload" />
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import supabase from '../services/supabase';

export default defineComponent({
  setup() {
    const title = ref('');
    const description = ref('');
    const imageFile = ref<File | null>(null);

    const handleImageUpload = (event: Event) => {
      const target = event.target as HTMLInputElement;
      if (target.files && target.files[0]) {
        imageFile.value = target.files[0];
      }
    };

    const handleSubmit = async () => {
      if (!title.value || !description.value || !imageFile.value) {
        alert('Fill out all fields');
        return;
      }

      try {
        // Unique file name with timestamp (to avoid conflicts)
        const uniqueFileName = `${Date.now()}-${imageFile.value.name}`;

        // Upload image to Supabase storage
        const { data: imageData, error: uploadError } = await supabase.storage
          .from('piece_image')
          .upload(`public/${uniqueFileName}`, imageFile.value);

        if (uploadError) throw uploadError;

        const imageUrl = imageData?.path;

        // Insert item info to db
        const { error: insertError } = await supabase
          .from('piece')
          .insert([
            {
              title: title.value,
              description: description.value,
              image: imageUrl,
              category: null,
              tag: null,
            },
          ]);

        if (insertError) throw insertError;

        // Clear form
        title.value = '';
        description.value = '';
        imageFile.value = null;
        alert('Item added successfully!');
      } catch (error) {
        alert(`Error: ${(error as Error).message}`);
      }
    };

    return {
      title,
      description,
      handleImageUpload,
      handleSubmit,
    };
  },
});
</script>

<style scoped>
.new-item-form {
  max-width: 400px;
  margin: 0 auto;
}
</style>

