import { Box, Container, Flex, Heading, Link, Menu, MenuButton, MenuList, MenuItem, Spacer, Input, InputGroup, InputRightElement, IconButton } from '@chakra-ui/react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import newsService from '../../services/news';
import { Category } from '../../services/news';
import { SearchIcon } from '@chakra-ui/icons';

interface MainLayoutProps {
    children: React.ReactNode;
}

const MainLayout = ({ children }: MainLayoutProps) => {
    const [categories, setCategories] = useState<Category[]>([]);
    const [searchQuery, setSearchQuery] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const data = await newsService.getCategories();
                setCategories(data);
            } catch (error) {
                console.error('Erro ao carregar categorias:', error);
            }
        };

        fetchCategories();
    }, []);

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        if (searchQuery.trim()) {
            navigate(`/?search=${encodeURIComponent(searchQuery.trim())}`);
        }
    };

    const handleLogoClick = () => {
        setSearchQuery(''); // Limpa o campo de busca
        navigate('/'); // Navega para a página inicial sem parâmetros
    };

    return (
        <Box minH="100vh" display="flex" flexDirection="column">
            <Box as="header" bg="brand.500" color="white" py={4}>
                <Container maxW="container.xl">
                    <Flex align="center" gap={4}>
                        <Link 
                            as={RouterLink} 
                            to="/" 
                            _hover={{ textDecoration: 'none' }}
                            onClick={handleLogoClick}
                        >
                            <Heading size="md">Paróquia News</Heading>
                        </Link>
                        <Spacer />
                        <form onSubmit={handleSearch} style={{ flex: '1', maxWidth: '400px' }}>
                            <InputGroup>
                                <Input
                                    placeholder="Buscar notícias..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    bg="white"
                                    color="gray.700"
                                    _placeholder={{ color: 'gray.500' }}
                                />
                                <InputRightElement>
                                    <IconButton
                                        aria-label="Buscar"
                                        icon={<SearchIcon />}
                                        type="submit"
                                        colorScheme="brand"
                                        variant="ghost"
                                    />
                                </InputRightElement>
                            </InputGroup>
                        </form>
                        <Menu>
                            <MenuButton 
                                as={Link} 
                                color="white" 
                                _hover={{ textDecoration: 'none', bg: 'brand.600' }}
                                px={4}
                                py={2}
                                borderRadius="md"
                            >
                                Categorias
                            </MenuButton>
                            <MenuList bg="white" borderColor="gray.200" minW="200px">
                                <MenuItem 
                                    as={RouterLink} 
                                    to="/"
                                    _hover={{ bg: 'brand.50' }}
                                    color="gray.700"
                                    onClick={() => setSearchQuery('')}
                                >
                                    Todas as Categorias
                                </MenuItem>
                                {categories.map((category) => (
                                    <MenuItem
                                        key={category.id}
                                        as={RouterLink}
                                        to={`/?category=${category.id}`}
                                        _hover={{ bg: 'brand.50' }}
                                        color="gray.700"
                                        onClick={() => setSearchQuery('')}
                                    >
                                        {category.name}
                                    </MenuItem>
                                ))}
                            </MenuList>
                        </Menu>
                    </Flex>
                </Container>
            </Box>

            <Box as="main" flex="1" py={8}>
                <Container maxW="container.xl">{children}</Container>
            </Box>

            <Box as="footer" bg="brand.50" py={4}>
                <Container maxW="container.xl">
                    <Flex justify="center">
                        <Box textAlign="center">
                            <Heading size="sm" color="brand.700">Paróquia News</Heading>
                            <Box mt={2} color="brand.600">© {new Date().getFullYear()} Todos os direitos reservados</Box>
                        </Box>
                    </Flex>
                </Container>
            </Box>
        </Box>
    );
};

export default MainLayout; 