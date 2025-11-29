import { useQuery } from '@tanstack/react-query';
import { fetchDashboardStats, fetchRecentActivity, fetchExpiringPolicies, fetchServiceHealthSummary } from '../data/mockApi';

export function useDashboardStats() {
  return useQuery({ queryKey: ['dashboard', 'stats'], queryFn: fetchDashboardStats });
}

export function useRecentActivity() {
  return useQuery({ queryKey: ['dashboard', 'activity'], queryFn: fetchRecentActivity });
}

export function useExpiringPolicies() {
  return useQuery({ queryKey: ['dashboard', 'expiring'], queryFn: fetchExpiringPolicies });
}

export function useServiceHealth() {
  return useQuery({ queryKey: ['dashboard', 'service-health'], queryFn: fetchServiceHealthSummary });
}
