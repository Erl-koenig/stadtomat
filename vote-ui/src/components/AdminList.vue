<script setup lang="ts">

import { pieceService } from '@/services/pieceService';
import { Piece, Category } from '@/types';
import { ColumnDef, createColumnHelper } from '@tanstack/vue-table';
import { h, onMounted, ref } from 'vue';
import EditPiece from './EditPiece.vue';
import DataTable from './DataTable.vue';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { loginService } from '@/services/loginService';
import { Label } from './ui/label';

const pieces = ref<Piece[]>([]);
const username = ref('');
const password = ref('');
const loggedIn = ref(false);

const getPieces = async () => {
    try {
        const res = await pieceService.fetchPieces();
        if (res) {
            console.log(res);
            pieces.value = res;
        }
    } catch (error) {
        console.error('Error fetching pieces:', error);
    }
};

const updatePiece = async (updatedPiece: Piece) => {
    const index = pieces.value.findIndex((p) => p.id === updatedPiece.id);
    console.log('Updating piece:', updatedPiece);
    try {
        let res = await pieceService.updatePiece(updatedPiece, pieces.value[index]);
        if (res) {
            alert('Piece updated successfully');
            getPieces();
        }

    } catch (error) {
        console.error('Error updating piece:', error);
    }
};

const deletePiece = async (id: string) => {
    console.log('Deleting piece:', id);
    try {
        const res = await pieceService.deletePiece(id);
        if (res) {
            pieces.value = pieces.value.filter((p) => p.id !== id);
        }
    } catch (error) {
        console.error('Error deleting piece:', error);
    }
};

onMounted(() => {
    loggedIn.value = loginService.isLoggedIn();
    if (loggedIn.value) {
        getPieces();
    } else {
        console.log('Not logged in');
    }

});


const columnHelper = createColumnHelper<Piece>();
const columns: ColumnDef<Piece, any>[] = [
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
        cell: ({ row }) => {
            let cat = row.getValue('category') as Category;
            if (cat && cat.id) {
                return cat.title
            }
            return ''
        },
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
            return [h(EditPiece, {
                piece: row.original,
                'onUpdate:piece': (updatedPiece: Piece) => {
                    updatePiece(updatedPiece);
                },
            }), h(Button, { class: 'bg-red-800', onClick: () => deletePiece(row.original.id) }, () => 'Delete')];
        },
    }),
];


const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
};

function doLogin() {
    console.log('Logging in...');
    loginService.login(username.value, password.value).then((res) => {
        loggedIn.value = loginService.isLoggedIn();
        if (res) {
            getPieces();
        }
    });

}

</script>

<template>
    <template v-if="!loggedIn">
        <div class="w-full">
            <div class="grid gap-4 py-4">
                <div class="grid grid-cols-4 items-center gap-4">
                    <Label for="username" class="text-right">
                        Username
                    </Label>
                    <Input id="username" v-model="username" class="col-span-3" />
                </div>
                <div class="grid grid-cols-4 items-center gap-4">
                    <Label for="password" class="text-right">
                        Password
                    </Label>
                    <Input type="password" id="password" v-model="password" class="col-span-3" />
                </div>
                <div class="grid grid-cols-2 items-center gap-4">
                    <Button class="bg-green-800" type="button" @click="doLogin">Log In</Button>
                </div>
            </div>

        </div>
    </template><template v-else>
        <div class="">
            <div v-if="pieces">
                <DataTable :columns="columns" :data="pieces" />
            </div>
        </div>
    </template>
</template>