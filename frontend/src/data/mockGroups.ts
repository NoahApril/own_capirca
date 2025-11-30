import type { Group } from '../types';

export const mockGroups: Group[] = [
  {
    id: 1,
    serviceId: 1,
    serviceName: 'ATREMOTE',
    name: 'Printer-Core',
    type: 'host',
    members: [
      { type: 'host', id: 1, name: 'host-192.168.10.5' },
      { type: 'host', id: 3, name: 'printer-ricoh-001' },
    ],
    comment: 'Critical printer devices',
    createdAt: '2024-01-15T10:00:00Z',
    updatedAt: '2024-11-28T14:30:00Z',
  },
  {
    id: 2,
    serviceId: 2,
    serviceName: 'AD',
    name: 'Domain-Controllers',
    type: 'host',
    members: [
      { type: 'host', id: 6, name: 'dc-primary-01' },
      { type: 'host', id: 7, name: 'dc-secondary-01' },
    ],
    comment: 'All AD Domain Controllers',
    createdAt: '2024-01-10T09:00:00Z',
    updatedAt: '2024-11-29T08:00:00Z',
  },
  {
    id: 3,
    serviceId: 3,
    serviceName: 'MOODLE',
    name: 'Moodle-Frontend',
    type: 'network',
    members: [
      { type: 'network', id: 5, name: 'moodle-front-net' },
    ],
    createdAt: '2024-02-01T11:00:00Z',
    updatedAt: '2024-11-27T16:45:00Z',
  },
  {
    id: 4,
    serviceId: 4,
    serviceName: 'SAP',
    name: 'SAP-Core',
    type: 'mixed',
    members: [
      { type: 'host', id: 12, name: 'sap-app-01' },
      { type: 'host', id: 13, name: 'sap-db-01' },
      { type: 'network', id: 6, name: 'sap-core-net' },
    ],
    createdAt: '2024-01-05T08:30:00Z',
    updatedAt: '2024-11-29T07:15:00Z',
  },
  {
    id: 5,
    serviceId: 6,
    serviceName: 'DMS',
    name: 'DMS-Core',
    type: 'host',
    members: [
      { type: 'host', id: 15, name: 'dms-app-01' },
      { type: 'host', id: 16, name: 'dms-db-01' },
    ],
    createdAt: '2024-02-10T09:00:00Z',
    updatedAt: '2024-11-29T09:30:00Z',
  },
];
