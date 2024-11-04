import supabase from "./supabase";
import { Piece } from "@/types";


class PieceService {
    // Method to fetch pieces
    async fetchPieces(): Promise<Piece[]> {
        const { data, error } = await supabase
            .from('piece')
            .select(`
                id, title, description, category (id, title, description), tag, image, created_at, upvote_count
            `);

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


    async updatePieceUpvoteCount(id: string, upvoteCount: number): Promise<boolean> {
        const { data, error } = await supabase
            .from('piece')
            .update({ upvote_count: upvoteCount })
            .eq('id', id);
        if (error) {
            console.error('Error updating item:', error);
            return false;
        }
        return true;

    }

    async updatePiece(piece: Piece, originalPiece: Piece): Promise<any> {
        const updateData: Partial<Piece> = {};
        if (piece.title && piece.title !== originalPiece.title) updateData.title = piece.title;
        if (piece.description && piece.description !== originalPiece.description) updateData.description = piece.description;
        if (piece.category && piece.category !== originalPiece.category) updateData.category = piece.category;
        if (piece.tag && piece.tag !== originalPiece.tag) updateData.tag = piece.tag;
        if (piece.image && piece.image !== originalPiece.image) updateData.image = piece.image;

        const { data, error } = await supabase
            .from('piece')
            .update(updateData)
            .eq('id', piece.id);
        if (error) {
            console.error('Error updating item:', error);
        }
        return data;
    }

    async fetchPieceById(id: string): Promise<Piece | null> {
        const { data, error } = await supabase
            .from('piece')
            .select(`
                id, title, description, category (id, title, description), tag, image, created_at, upvote_count
            `)
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

    async deletePiece(id: string): Promise<boolean> {
        const { error } = await supabase
            .from('piece')
            .delete()
            .eq('id', id);
        if (error) {
            console.error('Error deleting item:', error);
            return false;
        }
        return true;
    }

}

// Export an instance of the PieceService class
export const pieceService = new PieceService();