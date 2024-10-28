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

const imageModel = computed({
    get: () => localPiece.value.image ?? '',
    set: (value: string) => {
        localPiece.value.image = value;
    },
});


const savePiece = () => {
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
                    <div class="w-full">
                        <label>Title: </label>
                        <Input v-model="localPiece.title" label="Title" />
                    </div>
                    <div>
                        <label>Description: </label>
                        <textarea v-model="localPiece.description" label="Description"></textarea>
                    </div>
                    <div>
                        <label>Tag: </label>
                        <Input v-model="localPiece.tag" label="Tag" />
                    </div>
                    <div>
                        <label>Image: </label>
                        <Input v-model="imageModel" label="Image" />
                    </div>
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