// Type definitions for the Service-Oriented Firewall Management System

/**
 * @typedef {'healthy' | 'warning' | 'critical'} ServiceStatus
 */

/**
 * @typedef {Object} Service
 * @property {number} id
 * @property {string} shortName - e.g. "ATREMOTE"
 * @property {string} fullName - e.g. "Ricoh @Remote"
 * @property {string} [description]
 * @property {string} [category] - e.g. "Printing", "Infrastructure"
 * @property {string} firewall - e.g. "fw-central-01"
 * @property {string} [owner]
 * @property {ServiceStatus} status
 * @property {string} createdAt - ISO date string
 * @property {string} updatedAt - ISO date string
 * @property {number} hostsCount
 * @property {number} networksCount
 * @property {number} groupsCount
 * @property {number} policiesCount
 * @property {number} policiesExpiringCount
 */

/**
 * @typedef {Object} Host
 * @property {number} id
 * @property {number} serviceId
 * @property {string} serviceName
 * @property {string} name
 * @property {string} ipAddress
 * @property {string} [type] - e.g. "Server", "Printer", "Device"
 * @property {string} [comment]
 * @property {string} createdAt
 * @property {string} updatedAt
 * @property {number} usedInPoliciesCount
 */

/**
 * @typedef {Object} Network
 * @property {number} id
 * @property {number} serviceId
 * @property {string} serviceName
 * @property {string} name
 * @property {string} ipAddress - CIDR notation
 * @property {string} [comment]
 * @property {string} createdAt
 * @property {string} updatedAt
 * @property {number} usedInPoliciesCount
 */

/**
 * @typedef {Object} GroupMember
 * @property {'host' | 'network' | 'group'} type
 * @property {number} id
 * @property {string} name
 */

/**
 * @typedef {Object} Group
 * @property {number} id
 * @property {number} serviceId
 * @property {string} serviceName
 * @property {string} name
 * @property {'host' | 'network' | 'mixed'} type
 * @property {GroupMember[]} members
 * @property {string} [comment]
 * @property {string} createdAt
 * @property {string} updatedAt
 */

/**
 * @typedef {Object} PortService
 * @property {string} name - e.g. "HTTPS", "SSH"
 * @property {'TCP' | 'UDP' | 'ICMP'} protocol
 * @property {number} [port]
 * @property {string} [portRange] - e.g. "8080-8090"
 */

/**
 * @typedef {Object} Policy
 * @property {number} id
 * @property {number} serviceId
 * @property {string} serviceName
 * @property {string[]} source
 * @property {string[]} destination
 * @property {PortService[]} services
 * @property {'allow' | 'deny'} action
 * @property {number} ttlHours
 * @property {string} [comment]
 * @property {number} counter
 * @property {string} createdAt
 * @property {string} updatedAt
 * @property {string} [expiresAt]
 */

/**
 * @typedef {Object} DashboardStats
 * @property {number} servicesCount
 * @property {number} servicesHealthy
 * @property {number} servicesWarning
 * @property {number} servicesCritical
 * @property {number} hostsCount
 * @property {number} hostsChange
 * @property {number} networksCount
 * @property {number} networksChange
 * @property {number} groupsCount
 * @property {number} groupsChange
 * @property {number} policiesCount
 * @property {number} policiesChange
 * @property {number} policiesAllowCount
 * @property {number} policiesDenyCount
 * @property {Array<{serviceId: number, serviceName: string, resourceCount: number}>} topServices
 */

/**
 * @typedef {Object} ActivityItem
 * @property {number} id
 * @property {number} serviceId
 * @property {string} serviceName
 * @property {'host' | 'network' | 'group' | 'policy' | 'service'} type
 * @property {'created' | 'updated' | 'deleted'} action
 * @property {string} entityName
 * @property {string} timestamp
 * @property {string} [user]
 */

export {};
