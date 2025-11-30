import { useQuery } from '@tanstack/react-query';
import { 
  fetchServices, 
  fetchServiceById,
  fetchServiceHosts,
  fetchServiceNetworks,
  fetchServiceGroups,
  fetchServicePolicies 
} from '../data/mockApi';

export function useServices() {
  return useQuery({ queryKey: ['services'], queryFn: fetchServices });
}

export function useServiceById(serviceId) {
  return useQuery({
    queryKey: ['services', serviceId],
    queryFn: () => fetchServiceById(serviceId),
    enabled: !!serviceId,
  });
}

export function useServiceHosts(serviceId) {
  return useQuery({
    queryKey: ['services', serviceId, 'hosts'],
    queryFn: () => fetchServiceHosts(serviceId),
    enabled: !!serviceId,
  });
}

export function useServiceNetworks(serviceId) {
  return useQuery({
    queryKey: ['services', serviceId, 'networks'],
    queryFn: () => fetchServiceNetworks(serviceId),
    enabled: !!serviceId,
  });
}

export function useServiceGroups(serviceId) {
  return useQuery({
    queryKey: ['services', serviceId, 'groups'],
    queryFn: () => fetchServiceGroups(serviceId),
    enabled: !!serviceId,
  });
}

export function useServicePolicies(serviceId) {
  return useQuery({
    queryKey: ['services', serviceId, 'policies'],
    queryFn: () => fetchServicePolicies(serviceId),
    enabled: !!serviceId,
  });
}
