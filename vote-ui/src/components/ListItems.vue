<template>
  <div class="w-full">
    <div class="flex gap-2 items-center py-4">
      <Input class="max-w-sm" placeholder="Filter titles..."
        :model-value="table.getColumn('title')?.getFilterValue() as string"
        @update:model-value="table.getColumn('title')?.setFilterValue($event)" />
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button variant="outline" class="ml-auto">
            Columns
            <ChevronDown class="ml-2 h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <DropdownMenuCheckboxItem v-for="column in table.getAllColumns().filter((column) => column.getCanHide())"
            :key="column.id" class="capitalize" :checked="column.getIsVisible()" @update:checked="(value) => {
              column.toggleVisibility(!!value)
            }">
            {{ column.id }}
          </DropdownMenuCheckboxItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>

    <div class="rounded-md border">
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
          <template v-if="table.getRowModel().rows.length">
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
          </template>
          <TableRow v-else>
            <TableCell :colspan="columns.length" class="h-24 text-center">
              No results.
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>

    <div class="flex items-center justify-end space-x-2 py-4">
      <div class="flex-1 text-sm text-muted-foreground">
        {{ table.getFilteredSelectedRowModel().rows.length }} of
        {{ table.getFilteredRowModel().rows.length }} row(s) selected.
      </div>
      <div class="space-x-2">
        <Button variant="outline" size="sm" :disabled="!table.getCanPreviousPage()" @click="table.previousPage()">
          Previous
        </Button>
        <Button variant="outline" size="sm" :disabled="!table.getCanNextPage()" @click="table.nextPage()">
          Next
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { h, ref, onMounted } from 'vue';
import supabase from '../services/supabase.ts';
import {
  createColumnHelper,
  useVueTable,
  getCoreRowModel,
  getPaginationRowModel,
  getFilteredRowModel,
  FlexRender,
} from '@tanstack/vue-table';
import {
  Table,
  TableBody,
  TableCell,
  TableHeader,
  TableHead,
  TableRow,
} from '@/components/ui/table';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuCheckboxItem } from '@/components/ui/dropdown-menu';
import { cn } from '../lib/utils';
import { ChevronDown } from 'lucide-vue-next';

export interface Item {
  id: string;
  title: string;
  description: string;
  category: string;
  tag: string;
  image: string | null;
  created_at: string;
  upvote_count: number;
}

const fetchItems = async () => {
  const { data, error } = await supabase
    .from('piece')
    .select('id, title, description, category, tag, image, created_at, upvote_count');

  if (error) {
    console.error('Error fetching items:', error);
  }
  if (!data) {
    return [];
  }
  return data.map(item => ({
    ...item,
    image: item.image
      ? `https://lzirjhubrvqfumpsmenv.supabase.co/storage/v1/object/public/piece_image/${item.image}`
      : null,
  }));
};

const columnHelper = createColumnHelper<Item>();

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
      return image ? h('img', { src: image, alt: 'Item Image', class: 'max-w-[100px] h-auto' }) : 'No Image';  
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
          await handleVote(itemId, hasVoted.value);
          hasVoted.value = true;  
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

const handleVote = async (itemId: string, hasVoted: boolean) => {
  const votedItems = JSON.parse(localStorage.getItem('votedItems') || '[]');

  try {
    const { data: item, error: fetchError } = await supabase
      .from('piece')
      .select('upvote_count')
      .eq('id', itemId)
      .single();

    if (fetchError) {
      console.error('Error fetching upvote count:', fetchError);
      return;
    }

    const currentUpvoteCount = item?.upvote_count || 0;
    const newUpvoteCount = hasVoted ? currentUpvoteCount - 1 : currentUpvoteCount + 1;

    const { error: updateError } = await supabase
      .from('piece')
      .update({ upvote_count: newUpvoteCount })
      .eq('id', itemId);

    if (updateError) {
      console.error('Error updating vote count:', updateError);
      return;
    }

    if (hasVoted) {
      const updatedVotedItems = votedItems.filter(id => id !== itemId);
      localStorage.setItem('votedItems', JSON.stringify(updatedVotedItems));
    } else {
      votedItems.push(itemId);
      localStorage.setItem('votedItems', JSON.stringify(votedItems));
    }

  } catch (error) {
    console.error('Error handling vote:', error);
  }
};

const data = ref<Item[]>([]);

onMounted(async () => {
  data.value = await fetchItems();
});

const table = useVueTable({
  data: data,
  columns,
  getCoreRowModel: getCoreRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
});

</script>
