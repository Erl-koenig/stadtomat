<script setup lang="ts">
import {
    Table,
    TableBody,
    TableCell,
    TableHeader,
    TableHead,
    TableRow,
} from '@/components/ui/table';
import { cn } from '@/lib/utils';
import { pieceService } from '@/services/pieceService';
import { Piece } from '@/types';
import { createColumnHelper, getCoreRowModel, getFilteredRowModel, getPaginationRowModel, useVueTable, FlexRender } from '@tanstack/vue-table';
import { h, onMounted, ref } from 'vue';
import EditPiece from './EditPiece.vue';

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
                    const index = pieces.value.findIndex((p) => p.id === updatedPiece.id);
                    if (index !== -1) {
                        pieces.value[index] = updatedPiece;
                        console.log('Updated piece:', updatedPiece);
                    }
                },
            });
        },
    }),
];

const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
};

const table = useVueTable({
    data: pieces,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
})

</script>

<template>
    <div class="w-full">
        <div v-if="pieces">
            <Table>
                <TableHeader>
                    <TableRow v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
                        <TableHead v-for="header in headerGroup.headers" :key="header.id" :class="cn({
                            'sticky bg-background/95': header.column.getIsPinned(),
                            'left-0': header.column.getIsPinned() === 'left',
                            'right-0': header.column.getIsPinned() === 'right',
                        })">
                            <FlexRender v-if="!header.isPlaceholder" :render="header.column.columnDef.header"
                                :props="header.getContext()" />
                        </TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    <template v-for="row in table.getRowModel().rows" :key="row.id">
                        <TableRow :data-state="row.getIsSelected() && 'selected'">
                            <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id" :class="cn({
                                'sticky bg-background/95': cell.column.getIsPinned(),
                                'left-0': cell.column.getIsPinned() === 'left',
                                'right-0': cell.column.getIsPinned() === 'right',
                            })">
                                <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
                            </TableCell>
                        </TableRow>
                        <TableRow v-if="row.getIsExpanded()">
                            <TableCell :colspan="row.getAllCells().length">
                                {{ row.original }}
                            </TableCell>
                        </TableRow>
                    </template>
                </TableBody>
            </Table>
        </div>
    </div>
</template>