import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import AppLayout from './components/layout/AppLayout';
import Dashboard from './pages/Dashboard';
import ServicesOverview from './pages/ServicesOverview';
import ServiceDetailView from './pages/ServiceDetailView';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000,
    },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AppLayout />}>
            <Route index element={<Dashboard />} />
            <Route path="services" element={<ServicesOverview />} />
            <Route path="services/:serviceId" element={<ServiceDetailView />} />
            <Route path="services/:serviceId/hosts" element={<ServiceDetailView tab="hosts" />} />
            <Route path="services/:serviceId/networks" element={<ServiceDetailView tab="networks" />} />
            <Route path="services/:serviceId/groups" element={<ServiceDetailView tab="groups" />} />
            <Route path="services/:serviceId/policies" element={<ServiceDetailView tab="policies" />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
