import { extendTheme } from '@chakra-ui/react';

const theme = extendTheme({
    colors: {
        brand: {
            50: '#FFF9E6',
            100: '#FFEFB3',
            200: '#FFE680',
            300: '#FFDC4D',
            400: '#FFD31A',
            500: '#E6B800',
            600: '#B38F00',
            700: '#806600',
            800: '#4D3D00',
            900: '#1A1400',
        },
    },
    fonts: {
        heading: 'Inter, sans-serif',
        body: 'Inter, sans-serif',
    },
    components: {
        Button: {
            variants: {
                solid: {
                    bg: 'brand.500',
                    color: 'white',
                    _hover: {
                        bg: 'brand.600',
                    },
                },
            },
        },
        Link: {
            baseStyle: {
                _hover: {
                    textDecoration: 'none',
                },
            },
        },
        Tag: {
            variants: {
                solid: {
                    bg: 'brand.500',
                    color: 'white',
                },
            },
        },
    },
    styles: {
        global: {
            body: {
                bg: 'gray.50',
                color: 'gray.800',
            },
        },
    },
});

export default theme; 