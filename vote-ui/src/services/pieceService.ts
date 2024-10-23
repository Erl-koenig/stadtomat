import supabase from "./supabase";
import { Piece } from "@/types";


class PieceService {
    // Method to fetch pieces
    async fetchPieces(): Promise<Piece[]> {
        const { data, error } = await supabase
            .from('piece')
            .select('id, title, description, category, tag, image, created_at, upvote_count');

        if (error) {
            console.error('Error fetching items:', error);
            return [];
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
    }

    async searchPieces(searchTerm: string): Promise<Piece[]> {
        /**
         * search Pieces by title, description, category, tag
         */

        const { data, error } = await supabase
            .from('piece')
            .select('id, title, description, category, tag, image, created_at, upvote_count')
            .ilike('title', `%${searchTerm}%`)
        if (error) {
            console.error('Error fetching items:', error);
            return [];
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
    }


    async updatePieceUpvoteCount(id: string, upvoteCount: number): Promise<void> {
        await supabase
            .from('piece')
            .update({ upvote_count: upvoteCount })
            .eq('id', id);
    }

    async fetchPieceById(id: string): Promise<Piece | null> {
        const { data, error } = await supabase
            .from('piece')
            .select('id, title, description, category, tag, image, created_at, upvote_count')
            .eq('id', id)
            .single();

        if (error) {
            console.error('Error fetching item:', error);
            return null;
        }
        if (!data) {
            return null;
        }
        return {
            ...data,
            image: data.image
                ? `https://lzirjhubrvqfumpsmenv.supabase.co/storage/v1/object/public/piece_image/${data.image}`
                : null,
        };
    }

}

// Export an instance of the PieceService class
export const pieceService = new PieceService();