<script setup lang="ts">

import { pieceService } from '@/services/pieceService';
import { Piece } from '@/types';
import { createColumnHelper } from '@tanstack/vue-table';
import { h, onMounted, ref } from 'vue';
import EditPiece from './EditPiece.vue';
import DataTable from './DataTable.vue';

const pieces = ref<Piece[]>([]);


const getPieces = async () => {
    try {
        const res = await pieceService.fetchPieces();
        if (res) {
            pieces.value = res;
        }
    } catch (error) {
        console.error('Error fetching pieces:', error);
    }
};

const updatePiece = async (updatedPiece: Piece) => {
    const index = pieces.value.findIndex((p) => p.id === updatedPiece.id);
    try {
        const res = await pieceService.updatePiece(updatedPiece);
        if (index !== -1) {
            pieces.value[index] = res;
            console.log(res);
        }
    } catch (error) {
        console.error('Error updating piece:', error);
    }
};

onMounted(() => {
    getPieces();
});


const columnHelper = createColumnHelper<Piece>();
const columns = [
    columnHelper.accessor('title', {
        header: 'Title',
        cell: ({ row }) => row.getValue('title'),
    }),
    columnHelper.accessor('description', {
        header: 'Description',
        cell: ({ row }) => row.getValue('description'),
    }),
    columnHelper.accessor('category', {
        header: 'Category',
        cell: ({ row }) => row.getValue('category'),
    }),
    columnHelper.accessor('tag', {
        header: 'Tag',
        cell: ({ row }) => row.getValue('tag'),
    }),
    columnHelper.accessor('image', {
        header: 'Image',
        cell: ({ row }) => {
            const image = row.getValue('image');
            return image ? h('img', { src: image, alt: row.getValue('title'), class: 'max-w-[100px] h-auto' }) : 'No Image';
        },
    }),
    columnHelper.accessor('created_at', {
        header: 'Created At',
        cell: ({ row }) => formatDate(row.getValue('created_at')),
    }),
    columnHelper.accessor('upvote_count', {
        header: 'Upvotes',
        cell: ({ row }) => row.getValue('upvote_count'),
    }),
    columnHelper.display({
        header: 'Action',
        cell: ({ row }) => {
            return h(EditPiece, {
                piece: row.original,
                'onUpdate:piece': (updatedPiece: Piece) => {
                    updatePiece(updatedPiece);
                },
            });
        },
    }),
];


const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
};

</script>

<template>
    <div class="">
        <div v-if="pieces">
            <DataTable :columns="columns" :data="pieces" />
        </div>
    </div>
</template>