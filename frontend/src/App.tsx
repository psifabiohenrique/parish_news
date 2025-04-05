import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ChakraProvider } from '@chakra-ui/react';
import MainLayout from '@/components/layout/MainLayout';
import Home from '@/pages/Home';
import NewsDetail from '@/pages/NewsDetail';
import theme from '@/theme';

function App() {
    return (
        <ChakraProvider theme={theme}>
            <Router>
                <MainLayout>
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/news/:slug" element={<NewsDetail />} />
                    </Routes>
                </MainLayout>
            </Router>
        </ChakraProvider>
    );
}

export default App;
