import { useEffect, useState } from 'react';
import { Link as RouterLink, useSearchParams } from 'react-router-dom';
import {
    Box,
    Grid,
    Heading,
    Text,
    Image,
    Link,
    SimpleGrid,
    Container,
    VStack,
    HStack,
    Tag,
} from '@chakra-ui/react';
import newsService, { News } from '../services/news';

const Home = () => {
    const [featuredNews, setFeaturedNews] = useState<News[]>([]);
    const [latestNews, setLatestNews] = useState<News[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [searchParams] = useSearchParams();
    const categoryId = searchParams.get('category');
    const searchQuery = searchParams.get('search');

    useEffect(() => {
        const fetchNews = async () => {
            try {
                if (categoryId || searchQuery) {
                    // Se houver filtro de categoria ou busca, busca apenas as notícias filtradas
                    const news = await newsService.getPublishedNews({
                        ordering: '-created_at',
                        category: categoryId ? parseInt(categoryId) : undefined,
                        search: searchQuery || undefined,
                    });
                    setLatestNews(news);
                    setFeaturedNews([]);
                } else {
                    // Se não houver filtro, busca notícias em destaque e últimas notícias
                    const [featured, latest] = await Promise.all([
                        newsService.getFeaturedNews(),
                        newsService.getPublishedNews({ ordering: '-created_at' }),
                    ]);
                    setFeaturedNews(featured);
                    setLatestNews(latest);
                }
            } catch (error) {
                console.error('Erro ao carregar notícias:', error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchNews();
    }, [categoryId, searchQuery]);

    if (isLoading) {
        return <div>Carregando...</div>;
    }

    return (
        <Container maxW="container.xl">
            <VStack spacing={8} align="stretch">
                {/* Notícias em Destaque - Só exibe quando não há filtro */}
                {!categoryId && !searchQuery && featuredNews.length > 0 && (
                    <Box>
                        <Heading size="lg" mb={4}>
                            Notícias em Destaque
                        </Heading>
                        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
                            {featuredNews.map((news) => (
                                <Link
                                    key={news.id}
                                    as={RouterLink}
                                    to={`/news/${news.slug}`}
                                    _hover={{ textDecoration: 'none' }}
                                >
                                    <Box
                                        borderWidth="1px"
                                        borderRadius="lg"
                                        overflow="hidden"
                                        _hover={{ transform: 'translateY(-4px)', shadow: 'lg' }}
                                        transition="all 0.2s"
                                    >
                                        {news.cover_image && (
                                            <Image
                                                src={news.cover_image}
                                                alt={news.title}
                                                height="200px"
                                                width="100%"
                                                objectFit="cover"
                                            />
                                        )}
                                        <Box p={4}>
                                            <HStack spacing={2} mb={2}>
                                                <Tag colorScheme="brand">
                                                    {news.category.name}
                                                </Tag>
                                            </HStack>
                                            <Heading size="md" mb={2}>
                                                {news.title}
                                            </Heading>
                                            <Text color="gray.600" noOfLines={3}>
                                                {news.summary}
                                            </Text>
                                        </Box>
                                    </Box>
                                </Link>
                            ))}
                        </SimpleGrid>
                    </Box>
                )}

                {/* Últimas Notícias ou Notícias Filtradas */}
                <Box>
                    <Heading size="lg" mb={4}>
                        {searchQuery
                            ? `Resultados para "${searchQuery}"`
                            : categoryId
                                ? 'Notícias da Categoria'
                                : 'Últimas Notícias'}
                    </Heading>
                    {latestNews.length === 0 ? (
                        <Text>Nenhuma notícia encontrada.</Text>
                    ) : (
                        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
                            {latestNews.map((news) => (
                                <Link
                                    key={news.id}
                                    as={RouterLink}
                                    to={`/news/${news.slug}`}
                                    _hover={{ textDecoration: 'none' }}
                                >
                                    <Box
                                        borderWidth="1px"
                                        borderRadius="lg"
                                        overflow="hidden"
                                        _hover={{ transform: 'translateY(-4px)', shadow: 'lg' }}
                                        transition="all 0.2s"
                                    >
                                        {news.cover_image && (
                                            <Image
                                                src={news.cover_image}
                                                alt={news.title}
                                                height="200px"
                                                width="100%"
                                                objectFit="cover"
                                            />
                                        )}
                                        <Box p={4}>
                                            <HStack spacing={2} mb={2}>
                                                <Tag colorScheme="brand">
                                                    {news.category.name}
                                                </Tag>
                                            </HStack>
                                            <Heading size="md" mb={2}>
                                                {news.title}
                                            </Heading>
                                            <Text color="gray.600" noOfLines={3}>
                                                {news.summary}
                                            </Text>
                                        </Box>
                                    </Box>
                                </Link>
                            ))}
                        </SimpleGrid>
                    )}
                </Box>
            </VStack>
        </Container>
    );
};

export default Home; 