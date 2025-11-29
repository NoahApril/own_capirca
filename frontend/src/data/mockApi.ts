import type { ActivityItem, DashboardStats, Service } from '../types';
import { mockServices } from './mockServices';
import { mockHosts } from './mockHosts';
import { mockNetworks } from './mockNetworks';
import { mockGroups } from './mockGroups';
import { mockPolicies } from './mockPolicies';
import { mockDashboardStats, mockActivityItems } from './mockDashboard';

const delay = (ms = 250) => new Promise((resolve) => setTimeout(resolve, ms));

const clone = <T>(data: T): T => structuredClone(data);

export async function fetchServices(): Promise<Service[]> {
  await delay();
  return clone(mockServices);
}

export async function fetchServiceById(serviceId: number): Promise<Service | undefined> {
  await delay();
  return clone(mockServices.find((service) => service.id === serviceId));
}

export async function fetchServiceHosts(serviceId: number) {
  await delay();
  return clone(mockHosts.filter((host) => host.serviceId === serviceId));
}

export async function fetchServiceNetworks(serviceId: number) {
  await delay();
  return clone(mockNetworks.filter((network) => network.serviceId === serviceId));
}

export async function fetchServiceGroups(serviceId: number) {
  await delay();
  return clone(mockGroups.filter((group) => group.serviceId === serviceId));
}

export async function fetchServicePolicies(serviceId: number) {
  await delay();
  return clone(mockPolicies.filter((policy) => policy.serviceId === serviceId));
}

export async function fetchDashboardStats(): Promise<DashboardStats> {
  await delay();
  const totals = mockServices.reduce(
    (acc, service) => {
      acc.hosts += service.hostsCount;
      acc.networks += service.networksCount;
      acc.groups += service.groupsCount;
      acc.policies += service.policiesCount;
      return acc;
    },
    { hosts: 0, networks: 0, groups: 0, policies: 0 },
  );

  return clone({
    ...mockDashboardStats,
    servicesCount: mockServices.length,
    servicesHealthy: mockServices.filter((service) => service.status === 'healthy').length,
    servicesWarning: mockServices.filter((service) => service.status === 'warning').length,
    servicesCritical: mockServices.filter((service) => service.status === 'critical').length,
    hostsCount: totals.hosts,
    networksCount: totals.networks,
    groupsCount: totals.groups,
    policiesCount: totals.policies,
  });
}

export async function fetchRecentActivity(): Promise<ActivityItem[]> {
  await delay();
  return clone(mockActivityItems);
}

export async function fetchExpiringPolicies() {
  await delay();
  const now = Date.now();
  const soon = now + 72 * 60 * 60 * 1000;

  return clone(
    mockPolicies
      .filter((policy) => policy.expiresAt && new Date(policy.expiresAt).getTime() <= soon)
      .sort((a, b) => new Date(a.expiresAt ?? 0).getTime() - new Date(b.expiresAt ?? 0).getTime()),
  );
}

export async function fetchServiceHealthSummary() {
  await delay();
  return clone(
    mockServices.map((service) => ({
      id: service.id,
      name: service.shortName,
      status: service.status,
      expiringPolicies: service.policiesExpiringCount,
      policiesCount: service.policiesCount,
    })),
  );
}
