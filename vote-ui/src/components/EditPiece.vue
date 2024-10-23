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
                <div class="flex gap-2 items-center py-4" v-if="localPiece">
                    <Input v-model="localPiece.title" label="Title" />
                    <Input v-model="localPiece.description" label="Description" />
                    <!-- <Input v-model="localPiece.category" label="Category" /> -->
                    <!-- TODO: make dropdown for Category -->
                    <Input v-model="localPiece.tag" label="Tag" />
                    <Input v-model="imageModel" label="Image" />
                </div>
            </div>
            <DialogFooter>
                <DialogClose>
                    <Button type="button" @click="savePiece">Save</Button>
                </DialogClose>
            </DialogFooter>
        </DialogContent>
    </Dialog>


</template>