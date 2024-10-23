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
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

const pieces = ref<Piece[]>([]);

const getPieces = async () => {
    try {
        const res = await pieceService.fetchPieces();
        console.log(pieces);
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

async function onInputChange(event: { target: { value: string | any[]; }; }) {
    if (event.target.value.length > 2) {
        const res = await pieceService.searchPieces(event.target.value);
        if (res) {
            pieces.value = res;
        } else {
            pieces.value = [];
        }
    }
}

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
            const itemId = row.original.id;
            const hasVoted = ref(checkIfVoted(itemId));

            return h(Button, {
                disabled: hasVoted.value,
                onClick: async () => {
                    console.log("Vote do");

                },
            }, hasVoted.value ? 'Voted' : 'Vote');
        },
    }),
];

const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
};

const checkIfVoted = (itemId: string) => {
    const votedItems = JSON.parse(localStorage.getItem('votedItems') || '[]');
    return votedItems.includes(itemId);
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
        <div class="flex gap-2 items-center justify-between">
            <Input @input="onInputChange" placeholder="Search" />
            <h1 class="text-2xl font-bold">Admin</h1>
        </div>
        <div v-if="pieces">
            <p>Show pieces</p>
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