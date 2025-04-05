import api from './api';
import axios from 'axios';

export interface News {
    id: number;
    title: string;
    slug: string;
    content: string;
    summary: string;
    cover_image: string;
    author: string;
    category: Category;
    published_at: string | null;
    created_at: string;
    updated_at: string;
    is_published: boolean;
    featured: boolean;
    images: {
        id: number;
        image: string;
        caption: string;
        order: number;
    }[];
    tags: {
        id: number;
        name: string;
    }[];
}

export interface Category {
    id: number;
    name: string;
    slug: string;
}

export interface Image {
    id: number;
    image: string;
    caption: string;
    order: number;
}

export interface NewsCreateData {
    title: string;
    content: string;
    summary: string;
    category: number;
    cover_image?: File;
    is_published: boolean;
    featured: boolean;
    images?: {
        image: File | string;
        caption: string;
        order: number;
    }[];
}

interface NewsFilters {
    ordering?: string;
    category?: number;
    search?: string;
    featured?: boolean;
    published?: boolean;
}

const API_URL = 'http://localhost:8000/api';

const newsService = {
    async getCategories(): Promise<Category[]> {
        const response = await axios.get(`${API_URL}/categories/`);
        return response.data;
    },

    async getNews(filters: NewsFilters = {}): Promise<News[]> {
        const params = new URLSearchParams();
        if (filters.ordering) params.append('ordering', filters.ordering);
        if (filters.category) params.append('category', filters.category.toString());
        if (filters.search) params.append('search', filters.search);
        if (filters.featured) params.append('featured', 'true');
        if (filters.published) params.append('published', 'true');

        const response = await axios.get(`${API_URL}/news/?${params.toString()}`);
        return response.data;
    },

    async getNewsBySlug(slug: string): Promise<News> {
        const response = await axios.get(`${API_URL}/news/${slug}/`);
        return response.data;
    },

    async getPublishedNews(filters: NewsFilters = {}): Promise<News[]> {
        return newsService.getNews({ ...filters, published: true });
    },

    async getFeaturedNews(): Promise<News[]> {
        return newsService.getNews({ featured: true, published: true });
    },

    async createNews(data: NewsCreateData): Promise<News> {
        const formData = new FormData();
        formData.append('title', data.title);
        formData.append('content', data.content);
        formData.append('summary', data.summary);
        formData.append('category', data.category.toString());
        formData.append('is_published', data.is_published.toString());
        formData.append('featured', data.featured.toString());

        if (data.cover_image) {
            formData.append('cover_image', data.cover_image);
        }

        if (data.images) {
            data.images.forEach((image, index) => {
                if (image.image instanceof File) {
                    formData.append(`images[${index}].image`, image.image);
                    formData.append(`images[${index}].caption`, image.caption);
                    formData.append(`images[${index}].order`, image.order.toString());
                }
            });
        }

        const response = await api.post<News>('news/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    async updateNews(id: number, data: Partial<NewsCreateData>): Promise<News> {
        const formData = new FormData();

        if (data.title) formData.append('title', data.title);
        if (data.content) formData.append('content', data.content);
        if (data.summary) formData.append('summary', data.summary);
        if (data.category) formData.append('category', data.category.toString());
        if (data.is_published !== undefined) formData.append('is_published', data.is_published.toString());
        if (data.featured !== undefined) formData.append('featured', data.featured.toString());

        if (data.cover_image) {
            formData.append('cover_image', data.cover_image);
        }

        if (data.images) {
            data.images.forEach((image, index) => {
                if (image.image instanceof File) {
                    formData.append(`images[${index}].image`, image.image);
                    formData.append(`images[${index}].caption`, image.caption);
                    formData.append(`images[${index}].order`, image.order.toString());
                }
            });
        }

        const response = await api.patch<News>(`news/${id}/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    async deleteNews(id: number): Promise<void> {
        await api.delete(`news/${id}/`);
    },

    async updateNewsBySlug(slug: string, data: Partial<NewsCreateData>): Promise<News> {
        const formData = new FormData();

        if (data.title) formData.append('title', data.title);
        if (data.content) formData.append('content', data.content);
        if (data.summary) formData.append('summary', data.summary);
        if (data.category) formData.append('category', data.category.toString());
        if (data.is_published !== undefined) formData.append('is_published', data.is_published.toString());
        if (data.featured !== undefined) formData.append('featured', data.featured.toString());

        if (data.cover_image) {
            formData.append('cover_image', data.cover_image);
        }

        if (data.images) {
            data.images.forEach((image, index) => {
                if (image.image instanceof File) {
                    formData.append(`images[${index}].image`, image.image);
                    formData.append(`images[${index}].caption`, image.caption);
                    formData.append(`images[${index}].order`, image.order.toString());
                }
            });
        }

        const response = await api.patch<News>(`news/${slug}/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },
};

export default newsService; 