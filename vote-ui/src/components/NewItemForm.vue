<template>
  <div class="new-item-form">
    <form @submit="onSubmit">
      <!-- Title Field -->
      <FormField v-slot="{ field }" name="title">
        <FormItem>
          <FormLabel>Title</FormLabel>
          <FormControl>
            <Input v-bind="field" type="text" id="title" placeholder="Item title" />
          </FormControl>
          <FormDescription>
            The name of your item. Must be at least 2 characters long.
          </FormDescription>
          <FormMessage />
        </FormItem>
      </FormField>
      <br>
      <br>
      <!-- Description Field -->
      <FormField v-slot="{ field }" name="description">
        <FormItem>
          <FormLabel>Description</FormLabel>
          <FormControl>
            <textarea v-bind="field" id="description" placeholder="Item description"
              class="border rounded-md p-2 w-full min-h-[80px]"></textarea>
          </FormControl>
          <FormDescription>
            Describe your item in detail. Minimum of 5 characters.
          </FormDescription>
          <FormMessage />
        </FormItem>
      </FormField>
      <br>
      <br>
      <!-- File upload -->
      <div>
        <Label for="image">Picture</Label>
        <Input id="image" type="file" @change="handleImageUpload" :key="fileInputKey" />
      </div>

      <!-- Buttons -->
      <div class="flex justify-between mt-4">
        <Button type="button" @click="clearForm" class="bg-medium text-white hover:bg-light">Clear</Button>
        <Button type="submit" class="bg-darkest hover:bg-light">Submit</Button>
      </div>
    </form>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import supabase from '../services/supabase'

import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormDescription,
  FormMessage,
} from '@/components/ui/form'

// Define form validation schema with Zod
const formSchema = toTypedSchema(
  z.object({
    title: z.string().min(2, 'Title must be at least 2 characters').max(50, 'Title is too long'),
    description: z.string().min(5, 'Description must be at least 5 characters').max(500, 'Description is too long'),
  })
)

// Setup form handling with vee-validate
const { handleSubmit, resetForm } = useForm({
  validationSchema: formSchema,
})

const imageFile = ref<File | null>(null)
const fileInputKey = ref(0) // Key for the file input

// Handle image upload event
const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    imageFile.value = target.files[0]
  }
}
const clearForm = () => {
  resetForm()
  imageFile.value = null;
  fileInputKey.value++;
}

// Handle form submission
const onSubmit = handleSubmit(async (values) => {
  try {
    if (!imageFile.value) {
      alert('Please upload an image.')
      return
    }

    // Unique file name with timestamp (to avoid conflicts)
    const uniqueFileName = `${Date.now()}-${imageFile.value.name}`

    // Upload image to Supabase storage
    const { data: imageData, error: uploadError } = await supabase.storage
      .from('piece_image')
      .upload(`public/${uniqueFileName}`, imageFile.value)

    if (uploadError) throw uploadError

    const imageUrl = imageData?.path

    // Insert item info to db
    const { error: insertError } = await supabase
      .from('piece')
      .insert([
        {
          ...values,
          image: imageUrl,
          category: null,
          tag: null,
        }
      ])

    if (insertError) throw insertError

    clearForm();
    alert('Item added successfully!')
  } catch (error) {
    alert(`Error: ${(error as Error).message}`)
  }

})
</script>
