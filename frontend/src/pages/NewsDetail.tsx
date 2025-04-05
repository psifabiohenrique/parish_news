import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
    Box,
    Container,
    Heading,
    Text,
    Image,
    VStack,
    HStack,
    Tag,
    Link,
    Spinner,
    SimpleGrid,
} from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';
import newsService, { News } from '../services/news';
import { useToast } from '@chakra-ui/react';

const NewsDetail = () => {
    const { slug } = useParams<{ slug: string }>();
    const [news, setNews] = useState<News | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const toast = useToast();

    useEffect(() => {
        const fetchNews = async () => {
            if (!slug) return;
            
            try {
                const data = await newsService.getNewsBySlug(slug);
                setNews(data);
            } catch (error) {
                console.error('Erro ao carregar notícia:', error);
                toast({
                    title: 'Erro ao carregar notícia',
                    status: 'error',
                    duration: 3000,
                    isClosable: true,
                });
            } finally {
                setIsLoading(false);
            }
        };

        fetchNews();
    }, [slug, toast]);

    if (isLoading) {
        return (
            <Container maxW="container.xl" py={8}>
                <Box display="flex" justifyContent="center" alignItems="center" minH="200px">
                    <Spinner size="xl" color="blue.500" />
                </Box>
            </Container>
        );
    }

    if (!news) {
        return (
            <Container maxW="container.xl" py={8}>
                <Text>Notícia não encontrada</Text>
            </Container>
        );
    }

    return (
        <Container maxW="container.xl" py={8}>
            <VStack spacing={8} align="stretch">
                <Box>
                    <HStack spacing={2} mb={4}>
                        <Link
                            as={RouterLink}
                            to={`/?category=${news.category.id}`}
                            _hover={{ textDecoration: 'none' }}
                        >
                            <Tag
                                colorScheme="blue"
                                size="lg"
                                cursor="pointer"
                                _hover={{ bg: 'blue.600' }}
                            >
                                {news.category.name}
                            </Tag>
                        </Link>
                    </HStack>
                    <Heading size="2xl" mb={4}>
                        {news.title}
                    </Heading>
                    <Text color="gray.500" mb={4}>
                        Por {news.author} em {news.published_at ? new Date(news.published_at).toLocaleDateString() : 'Não publicado'}
                    </Text>
                </Box>

                {news.cover_image && (
                    <Image
                        src={news.cover_image}
                        alt={news.title}
                        borderRadius="lg"
                        objectFit="cover"
                        maxH="500px"
                        w="100%"
                    />
                )}

                <Box>
                    <Text fontSize="xl" mb={4}>
                        {news.summary}
                    </Text>
                    <Text whiteSpace="pre-wrap">{news.content}</Text>
                </Box>

                {news.images && news.images.length > 0 && (
                    <Box>
                        <Heading as="h2" size="lg" mb={4}>
                            Galeria de Imagens
                        </Heading>
                        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
                            {news.images.map((image, index) => (
                                <Box key={index}>
                                    <Image
                                        src={image.image}
                                        alt={image.caption || `Imagem ${index + 1}`}
                                        borderRadius="lg"
                                        mb={2}
                                    />
                                    {image.caption && (
                                        <Text fontSize="sm" color="gray.500">
                                            {image.caption}
                                        </Text>
                                    )}
                                </Box>
                            ))}
                        </SimpleGrid>
                    </Box>
                )}
            </VStack>
        </Container>
    );
};

export default NewsDetail; 