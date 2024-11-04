<script setup lang="ts">
import { ref, watch, defineProps, defineEmits, computed } from 'vue';
import { Piece } from '@/types';
import Input from './ui/input/Input.vue';
import Dialog from './ui/dialog/Dialog.vue';
import DialogTrigger from './ui/dialog/DialogTrigger.vue';
import Button from './ui/button/Button.vue';
import DialogContent from './ui/dialog/DialogContent.vue';
import DialogHeader from './ui/dialog/DialogHeader.vue';
import DialogTitle from './ui/dialog/DialogTitle.vue';
import DialogFooter from './ui/dialog/DialogFooter.vue';
import DialogClose from './ui/dialog/DialogClose.vue';

import * as z from 'zod'
import { FormField } from './ui/form';
import FormItem from './ui/form/FormItem.vue';
import FormLabel from './ui/form/FormLabel.vue';
import FormControl from './ui/form/FormControl.vue';
import FormDescription from './ui/form/FormDescription.vue';
import FormMessage from './ui/form/FormMessage.vue';
import { toTypedSchema } from '@vee-validate/zod';
import { Form, useForm } from 'vee-validate';

const props = defineProps<{
    piece: Piece | null;
}>();
const emit = defineEmits(['update:piece']);
const localPiece = ref<Piece>({
    id: '', title: '', description: '', tag: '', image: '',
    category: { id: '', title: '', description: '', created_at: '' },
    created_at: '',
    upvote_count: 0
});

const imageFile = ref<File | null>(null);
const fileInputKey = ref(0);

const formSchema = toTypedSchema(
    z.object({
        title: z.string().min(2, 'Title must be at least 2 characters').max(50, 'Title is too long'),
        description: z.string().min(5, 'Description must be at least 5 characters').max(500, 'Description is too long'),
        category: z.string().optional(),
        tag: z.string().optional(),
        image: z.string().url().nullable().optional(),
    })
)

useForm({
    validationSchema: formSchema,
    initialValues: props.piece ? {
        title: props.piece.title,
        description: props.piece.description,
        tag: props.piece.tag
    } : {
        title: '',
        description: '',
        tag: ''
    }
});


watch(
    () => props.piece,
    (newPiece) => {
        localPiece.value = newPiece ? { ...newPiece } : {
            id: '', title: '', description: '', tag: '', image: '',
            category: { id: '', title: '', description: '', created_at: '' },
            created_at: '',
            upvote_count: 0
        };
    },
    { immediate: true }
);



const handleImageUpload = (event: Event) => {
    const target = event.target as HTMLInputElement
    if (target.files && target.files[0]) {
        imageFile.value = target.files[0]
    }
}

const imageModel = computed({
    get: () => localPiece.value.image ?? '',
    set: (value: string) => {
        localPiece.value.image = value;
    },
});

const savePiece = (event: any) => {
    console.log(`Saving piece: ${event}`);
    console.log(`piece id: ${localPiece.value.id}`);
    if (localPiece.value) {
        console.log(`Saving piece: ${localPiece.value.title}`);
        emit('update:piece', localPiece.value);
    }
};
</script>

<template>
    <Dialog>
        <DialogTrigger>
            <Button> Edit </Button>
        </DialogTrigger>
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Edit Piece</DialogTitle>
            </DialogHeader>

            <div div="w-full">
                <div class="flex flex-wrap gap-2 items-center py-4 mb-2" v-if="localPiece">
                    <Form id="editForm">
                        <FormField name="title">
                            <FormItem>
                                <FormLabel for="title">Title</FormLabel>
                                <FormControl>
                                    <Input v-model="localPiece.title" type="text" id="title" placeholder="Item title" />
                                </FormControl>
                                <FormDescription>
                                    The name of your item. Must be at least 2 characters long.
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        </FormField>
                        <br>
                        <br>
                        <FormField name="description">
                            <FormItem>
                                <FormLabel for="description">Description</FormLabel>
                                <FormControl>
                                    <textarea v-model="localPiece.description" id="description"
                                        placeholder="Item description"
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
                        <!-- <FormField name="tag">
                            <FormItem>
                                <FormLabel for="tag">Tag</FormLabel>
                                <FormControl>
                                    <Input v-model="localPiece.tag" type="text" id="tag" placeholder="Item tag" />
                                </FormControl>
                                <FormDescription>
                                    The tag of your item.
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        </FormField> -->
                        <br>
                        <FormField name="image">
                            <FormItem>
                                <FormLabel for="image">Picture</FormLabel>
                                <div v-if="imageModel">
                                    <img :src="imageModel" alt="item image" class="w-20 h-20 rounded-md" />
                                </div>
                                <Input id="image" type="file" @change="handleImageUpload" :key="fileInputKey" />
                            </FormItem>
                        </FormField>
                    </Form>
                </div>
            </div>
            <DialogFooter>
                <DialogClose>
                    <Button type="button"
                        class="focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800"
                        @click="savePiece">Save</Button>
                    <Button type="button">Cancel</Button>
                </DialogClose>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>