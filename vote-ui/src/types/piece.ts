import { Category } from './category';

export interface Piece {
    id: string;
    title: string;
    description: string;
    category: Category;
    tag: string;
    image: string | null;
    created_at: string;
    upvote_count: number;
}