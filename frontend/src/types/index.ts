export type ServiceStatus = 'healthy' | 'warning' | 'critical';

export interface Service {
  id: number;
  shortName: string;
  fullName: string;
  description?: string;
  category?: string;
  firewall: string;
  owner?: string;
  status: ServiceStatus;
  createdAt: string;
  updatedAt: string;
  hostsCount: number;
  networksCount: number;
  groupsCount: number;
  policiesCount: number;
  policiesExpiringCount: number;
}

export interface Host {
  id: number;
  serviceId: number;
  serviceName: string;
  name: string;
  ipAddress: string;
  type?: string;
  comment?: string;
  createdAt: string;
  updatedAt: string;
  usedInPoliciesCount: number;
}

export interface Network {
  id: number;
  serviceId: number;
  serviceName: string;
  name: string;
  ipAddress: string;
  comment?: string;
  createdAt: string;
  updatedAt: string;
  usedInPoliciesCount: number;
}

export type GroupMemberType = 'host' | 'network' | 'group';

export interface GroupMember {
  type: GroupMemberType;
  id: number;
  name: string;
}

export interface Group {
  id: number;
  serviceId: number;
  serviceName: string;
  name: string;
  type: 'host' | 'network' | 'mixed';
  members: GroupMember[];
  comment?: string;
  createdAt: string;
  updatedAt: string;
}

export interface PortService {
  name: string;
  protocol: 'TCP' | 'UDP' | 'ICMP';
  port?: number;
  portRange?: string;
}

export interface Policy {
  id: number;
  serviceId: number;
  serviceName: string;
  source: string[];
  destination: string[];
  services: PortService[];
  action: 'allow' | 'deny';
  ttlHours: number;
  comment?: string;
  counter: number;
  createdAt: string;
  updatedAt: string;
  expiresAt?: string;
}

export interface DashboardStats {
  servicesCount: number;
  servicesHealthy: number;
  servicesWarning: number;
  servicesCritical: number;
  hostsCount: number;
  hostsChange: number;
  networksCount: number;
  networksChange: number;
  groupsCount: number;
  groupsChange: number;
  policiesCount: number;
  policiesChange: number;
  policiesAllowCount: number;
  policiesDenyCount: number;
  topServices: Array<{
    serviceId: number;
    serviceName: string;
    resourceCount: number;
  }>;
}

export interface ActivityItem {
  id: number;
  serviceId: number;
  serviceName: string;
  type: 'host' | 'network' | 'group' | 'policy' | 'service';
  action: 'created' | 'updated' | 'deleted';
  entityName: string;
  timestamp: string;
  user?: string;
}
