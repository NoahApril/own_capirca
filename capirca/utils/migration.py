# Copyright 2024 The Capirca Project Authors All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Data Migration Engine for converting external firewall rules to Capirca.

This module implements Phase 1 of the Capirca migration architecture,
providing tools to parse external firewall rule formats (like Confluence tables)
and convert them to Capirca policy files with automatic object extraction.

Classes:
    FirewallRule: Data model for a single firewall rule
    ConfluenceParser: Parse Confluence HTML tables to structured rules
    CapircaGenerator: Generate Capirca policy from rules
    ObjectExtractor: Extract network and service objects from rules
"""

import hashlib
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
from html.parser import HTMLParser

import requests
from absl import logging


class Error(Exception):
  """Base exception for migration module."""


class ParseError(Error):
  """Error parsing input data."""


class ValidationError(Error):
  """Error validating rule data."""


class MigrationAPIError(Error):
  """Error when communicating with the Phase 2 API."""


@dataclass
class ServiceDef:
  """Service definition with ports and protocols."""
  name: str
  ports: List[str]
  protocols: List[str]
  description: Optional[str] = None


@dataclass
class FirewallRule:
  """Structured representation of a firewall rule.
  
  Attributes:
    name: Unique name/identifier for the rule
    source_addresses: List of source IP addresses or networks
    destination_addresses: List of destination IP addresses or networks
    source_ports: List of source ports (can be ranges like '1024-65535')
    destination_ports: List of destination ports
    protocols: List of protocols (tcp, udp, icmp, etc.)
    action: Rule action (accept, deny, reject, etc.)
    comment: Description or comment for the rule
    options: Additional options (established, tcp-established, etc.)
  """
  name: str
  source_addresses: List[str] = field(default_factory=list)
  destination_addresses: List[str] = field(default_factory=list)
  source_ports: List[str] = field(default_factory=list)
  destination_ports: List[str] = field(default_factory=list)
  protocols: List[str] = field(default_factory=list)
  action: str = 'accept'
  comment: Optional[str] = None
  options: List[str] = field(default_factory=list)


class ConfluenceHTMLParser(HTMLParser):
  """HTML parser for extracting table data from Confluence."""
  
  def __init__(self):
    super().__init__()
    self.in_table = False
    self.in_row = False
    self.in_header = False
    self.in_cell = False
    self.current_row = []
    self.headers = []
    self.rows = []
    self.current_cell = []
    
  def handle_starttag(self, tag, attrs):
    if tag == 'table':
      self.in_table = True
    elif tag == 'tr' and self.in_table:
      self.in_row = True
      self.current_row = []
    elif tag == 'th' and self.in_row:
      self.in_header = True
      self.in_cell = True
      self.current_cell = []
    elif tag == 'td' and self.in_row:
      self.in_cell = True
      self.current_cell = []
      
  def handle_endtag(self, tag):
    if tag == 'table':
      self.in_table = False
    elif tag == 'tr':
      if self.in_row:
        if self.in_header:
          self.headers = self.current_row
          self.in_header = False
        else:
          self.rows.append(self.current_row)
        self.current_row = []
        self.in_row = False
    elif tag in ('th', 'td'):
      if self.in_cell:
        self.current_row.append(' '.join(self.current_cell).strip())
        self.current_cell = []
        self.in_cell = False
        
  def handle_data(self, data):
    if self.in_cell:
      self.current_cell.append(data.strip())


class ConfluenceParser:
  """Parse Confluence HTML table to structured firewall rules.
  
  Supports parsing Confluence tables with columns:
  - Rule/Name: Rule identifier
  - Source: Source addresses
  - Destination: Destination addresses
  - Port/Ports: Destination ports
  - Protocol: Network protocols
  - Action: Rule action (Allow/Deny/etc.)
  - Description/Comment: Rule description
  """
  
  HEADER_MAPPINGS = {
    'rule': 'name',
    'regel': 'name',
    'name': 'name',
    'source': 'source',
    'quelle': 'source',
    'src': 'source',
    'destination': 'destination',
    'ziel': 'destination',
    'dest': 'destination',
    'dst': 'destination',
    'port': 'port',
    'ports': 'port',
    'protocol': 'protocol',
    'proto': 'protocol',
    'action': 'action',
    'description': 'description',
    'comment': 'description',
    'beschreibung': 'description',
  }
  
  def parse_table(self, html_content: str) -> List[FirewallRule]:
    """Parse Confluence HTML table to structured rules.
    
    Args:
      html_content: HTML content containing Confluence table
      
    Returns:
      List of FirewallRule objects
      
    Raises:
      ParseError: If table structure is invalid
    """
    parser = ConfluenceHTMLParser()
    parser.feed(html_content)
    
    if not parser.headers:
      raise ParseError("No table headers found in HTML content")
    
    if not parser.rows:
      logging.warning("No data rows found in table")
      return []
    
    header_map = self._map_headers(parser.headers)
    rules = []
    
    for row_idx, row in enumerate(parser.rows):
      try:
        rule = self._parse_row(row, header_map)
        if rule:
          rules.append(rule)
      except Exception as e:
        logging.warning(f"Failed to parse row {row_idx + 1}: {e}")
        
    return rules
  
  def _map_headers(self, headers: List[str]) -> Dict[int, str]:
    """Map table column indices to field names."""
    header_map = {}
    for idx, header in enumerate(headers):
      normalized = header.lower().strip()
      field_name = self.HEADER_MAPPINGS.get(normalized)
      if field_name:
        header_map[idx] = field_name
    return header_map
  
  def _parse_row(self, row: List[str], header_map: Dict[int, str]) -> Optional[FirewallRule]:
    """Parse a single table row into a FirewallRule."""
    if not any(cell.strip() for cell in row):
      return None
      
    data = {}
    for idx, value in enumerate(row):
      field_name = header_map.get(idx)
      if field_name:
        data[field_name] = value.strip()
    
    if not data.get('name'):
      row_signature = ''.join(row).encode('utf-8')
      digest = hashlib.sha256(row_signature).hexdigest()[:8]
      data['name'] = f"rule-{digest}"
    
    rule = FirewallRule(name=self._normalize_name(data.get('name', 'unnamed')))
    
    if 'source' in data:
      rule.source_addresses = self._parse_addresses(data['source'])
    if 'destination' in data:
      rule.destination_addresses = self._parse_addresses(data['destination'])
    if 'port' in data:
      rule.destination_ports = self._parse_ports(data['port'])
    if 'protocol' in data:
      rule.protocols = self._parse_protocols(data['protocol'])
    if 'action' in data:
      rule.action = self._parse_action(data['action'])
    if 'description' in data:
      rule.comment = data['description']
      
    return rule
  
  def _normalize_name(self, name: str) -> str:
    """Normalize rule name to be valid Capirca term name."""
    name = re.sub(r'[^a-zA-Z0-9_-]', '-', name)
    name = re.sub(r'-+', '-', name)
    name = name.strip('-')
    return name.lower()
  
  def _parse_addresses(self, addr_str: str) -> List[str]:
    """Parse comma or space separated addresses."""
    if not addr_str:
      return []
    addresses = re.split(r'[,;\s]+', addr_str)
    return [addr.strip() for addr in addresses if addr.strip()]
  
  def _parse_ports(self, port_str: str) -> List[str]:
    """Parse comma or space separated ports."""
    if not port_str:
      return []
    ports = re.split(r'[,;\s]+', port_str)
    return [port.strip() for port in ports if port.strip()]
  
  def _parse_protocols(self, proto_str: str) -> List[str]:
    """Parse protocols from string."""
    if not proto_str:
      return []
    protocols = re.split(r'[,;\s]+', proto_str.lower())
    return [proto.strip() for proto in protocols if proto.strip()]
  
  def _parse_action(self, action_str: str) -> str:
    """Parse and normalize action."""
    action = action_str.lower().strip()
    action_map = {
      'allow': 'accept',
      'permit': 'accept',
      'accept': 'accept',
      'deny': 'deny',
      'drop': 'deny',
      'reject': 'reject',
    }
    return action_map.get(action, 'accept')


class ObjectExtractor:
  """Extract network and service objects from firewall rules.
  
  This class analyzes a list of firewall rules and automatically extracts
  reusable network objects and service definitions that can be used in
  Capirca definition files.
  """
  
  def extract_network_objects(self, rules: List[FirewallRule]) -> Dict[str, List[str]]:
    """Extract unique network objects from rules.
    
    Groups addresses that appear multiple times together into named objects.
    
    Args:
      rules: List of FirewallRule objects
      
    Returns:
      Dictionary mapping object names to lists of addresses
    """
    address_groups = {}
    
    for rule in rules:
      for addresses in (rule.source_addresses, rule.destination_addresses):
        if not addresses:
          continue
          
        key = tuple(sorted(addresses))
        if key not in address_groups:
          address_groups[key] = {
            'addresses': list(addresses),
            'count': 0
          }
        address_groups[key]['count'] += 1
    
    network_objects = {}
    used_names = set()
    
    for key, data in address_groups.items():
      if data['count'] >= 2 or len(data['addresses']) > 1:
        name = self._generate_network_name(data['addresses'], used_names)
        network_objects[name] = data['addresses']
        used_names.add(name)
    
    return network_objects
  
  def extract_service_objects(self, rules: List[FirewallRule]) -> Dict[str, ServiceDef]:
    """Extract unique service objects from rules.
    
    Groups port/protocol combinations that appear multiple times.
    
    Args:
      rules: List of FirewallRule objects
      
    Returns:
      Dictionary mapping service names to ServiceDef objects
    """
    service_groups = {}
    
    for rule in rules:
      if not rule.destination_ports or not rule.protocols:
        continue
        
      key = (tuple(sorted(rule.destination_ports)), tuple(sorted(rule.protocols)))
      if key not in service_groups:
        service_groups[key] = {
          'ports': list(rule.destination_ports),
          'protocols': list(rule.protocols),
          'count': 0
        }
      service_groups[key]['count'] += 1
    
    service_objects = {}
    used_names = set()
    
    for key, data in service_groups.items():
      if data['count'] >= 2:
        name = self._generate_service_name(data['ports'], data['protocols'], used_names)
        service_objects[name] = ServiceDef(
          name=name,
          ports=data['ports'],
          protocols=data['protocols']
        )
        used_names.add(name)
    
    return service_objects
  
  def _generate_network_name(self, addresses: List[str], used_names: Set[str]) -> str:
    """Generate a descriptive name for network object."""
    if len(addresses) == 1:
      addr = addresses[0]
      if '/' in addr:
        prefix = addr.split('/')[0].replace('.', '_').replace(':', '_')
        base_name = f"NET_{prefix}"
      else:
        base_name = f"HOST_{addr.replace('.', '_').replace(':', '_')}"
    else:
      base_name = f"NET_GROUP_{len(addresses)}"
    
    name = base_name
    counter = 1
    while name in used_names:
      name = f"{base_name}_{counter}"
      counter += 1
    
    return name
  
  def _generate_service_name(self, ports: List[str], protocols: List[str], used_names: Set[str]) -> str:
    """Generate a descriptive name for service object."""
    if len(ports) == 1 and len(protocols) == 1:
      base_name = f"SVC_{protocols[0].upper()}_{ports[0]}"
    elif len(protocols) == 1:
      base_name = f"SVC_{protocols[0].upper()}_MULTI"
    else:
      base_name = f"SVC_GROUP_{len(ports)}"
    
    name = base_name
    counter = 1
    while name in used_names:
      name = f"{base_name}_{counter}"
      counter += 1
    
    return name


class CapircaGenerator:
  """Generate Capirca policy files from firewall rules.
  
  This class converts structured FirewallRule objects into valid Capirca
  policy file format, with support for using extracted network and service
  objects.
  """
  
  def __init__(self, network_objects: Optional[Dict[str, List[str]]] = None,
               service_objects: Optional[Dict[str, ServiceDef]] = None):
    """Initialize generator with optional object definitions.
    
    Args:
      network_objects: Dictionary of network object definitions
      service_objects: Dictionary of service object definitions
    """
    self.network_objects = network_objects or {}
    self.service_objects = service_objects or {}
    self._reverse_network_map = self._build_reverse_network_map()
    self._reverse_service_map = self._build_reverse_service_map()
  
  def _build_reverse_network_map(self) -> Dict[str, str]:
    """Build reverse mapping from addresses to object names."""
    reverse_map = {}
    for name, addresses in self.network_objects.items():
      key = tuple(sorted(addresses))
      reverse_map[key] = name
    return reverse_map
  
  def _build_reverse_service_map(self) -> Dict[Tuple, str]:
    """Build reverse mapping from port/proto to service names."""
    reverse_map = {}
    for name, service_def in self.service_objects.items():
      key = (tuple(sorted(service_def.ports)), tuple(sorted(service_def.protocols)))
      reverse_map[key] = name
    return reverse_map
  
  def generate_policy(self, rules: List[FirewallRule], 
                     policy_name: str = 'generated-policy',
                     targets: Optional[List[Tuple[str, str]]] = None,
                     comment: Optional[str] = None) -> str:
    """Generate Capirca policy from rules.
    
    Args:
      rules: List of FirewallRule objects
      policy_name: Name for the policy
      targets: List of (platform, filter_name) tuples for target:: directives
      comment: Optional header comment
      
    Returns:
      Complete Capirca policy file content as string
    """
    if not targets:
      targets = [('cisco', policy_name), ('juniper', policy_name)]
    
    lines = []
    lines.append('header {')
    
    if comment:
      for line in comment.split('\n'):
        lines.append(f'  comment:: "{line}"')
    
    for platform, filter_name in targets:
      lines.append(f'  target:: {platform} {filter_name}')
    
    lines.append('}')
    lines.append('')
    
    for rule in rules:
      lines.extend(self._generate_term(rule))
      lines.append('')
    
    return '\n'.join(lines)
  
  def _generate_term(self, rule: FirewallRule) -> List[str]:
    """Generate Capirca term from a single rule."""
    lines = []
    lines.append(f'term {rule.name} {{')
    
    if rule.comment:
      lines.append(f'  comment:: "{rule.comment}"')
    
    if rule.source_addresses:
      src_ref = self._get_address_reference(rule.source_addresses)
      lines.append(f'  source-address:: {src_ref}')
    
    if rule.destination_addresses:
      dst_ref = self._get_address_reference(rule.destination_addresses)
      lines.append(f'  destination-address:: {dst_ref}')
    
    if rule.source_ports:
      lines.append(f'  source-port:: {" ".join(rule.source_ports)}')
    
    if rule.destination_ports:
      port_ref = self._get_port_reference(rule.destination_ports, rule.protocols)
      lines.append(f'  destination-port:: {port_ref}')
    
    if rule.protocols:
      lines.append(f'  protocol:: {" ".join(rule.protocols)}')
    
    if rule.options:
      lines.append(f'  option:: {" ".join(rule.options)}')
    
    lines.append(f'  action:: {rule.action}')
    lines.append('}')
    
    return lines
  
  def _get_address_reference(self, addresses: List[str]) -> str:
    """Get reference for addresses (object name or inline)."""
    key = tuple(sorted(addresses))
    if key in self._reverse_network_map:
      return self._reverse_network_map[key]
    return ' '.join(addresses)
  
  def _get_port_reference(self, ports: List[str], protocols: List[str]) -> str:
    """Get reference for ports (object name or inline)."""
    key = (tuple(sorted(ports)), tuple(sorted(protocols)))
    if key in self._reverse_service_map:
      return self._reverse_service_map[key]
    return ' '.join(ports)
  
  def generate_network_definitions(self) -> str:
    """Generate .net file content for network objects.
    
    Returns:
      Content for a Capirca .net definition file
    """
    lines = []
    for name, addresses in sorted(self.network_objects.items()):
      lines.append(f'{name} = {addresses[0]}')
      for addr in addresses[1:]:
        lines.append(f'{" " * (len(name) + 3)}{addr}')
      lines.append('')
    return '\n'.join(lines)
  
  def generate_service_definitions(self) -> str:
    """Generate .svc file content for service objects.
    
    Returns:
      Content for a Capirca .svc definition file
    """
    lines = []
    for name, service_def in sorted(self.service_objects.items()):
      port_proto_pairs = []
      for port in service_def.ports:
        for proto in service_def.protocols:
          port_proto_pairs.append(f'{port}/{proto}')
      
      lines.append(f'{name} = {port_proto_pairs[0]}')
      for pair in port_proto_pairs[1:]:
        lines.append(f'{" " * (len(name) + 3)}{pair}')
      lines.append('')
    
    return '\n'.join(lines)


class MigrationAPIClient:
  """Client helper for persisting migration outputs via the Phase 2 API."""

  def __init__(self, base_url: str, api_key: Optional[str] = None,
               session: Optional[requests.Session] = None,
               timeout: int = 30):
    """Initialize the API client.

    Args:
      base_url: Base URL of the Capirca API (e.g. http://localhost:8000/api).
      api_key: Optional bearer token for authentication.
      session: Optional custom requests session for testing.
      timeout: Request timeout in seconds.
    """
    self.base_url = base_url.rstrip('/')
    self.session = session or requests.Session()
    self.timeout = timeout
    self.headers = {'Content-Type': 'application/json'}
    if api_key:
      self.headers['Authorization'] = f'Bearer {api_key}'

  def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{self.base_url}{path}"
    response = self.session.post(
        url, json=payload, headers=self.headers, timeout=self.timeout)
    if response.status_code >= 400:
      raise MigrationAPIError(
          f"API request {url} failed with status {response.status_code}: "
          f"{response.text}")
    return response.json()

  def persist_network_object(self, name: str, addresses: List[str],
                             description: Optional[str] = None
                            ) -> Dict[str, Any]:
    payload = {
        'name': name,
        'addresses': addresses,
        'description': description,
    }
    return self._post('/network-objects', payload)

  def persist_service_object(self, service: ServiceDef) -> Dict[str, Any]:
    payload = {
        'name': service.name,
        'ports': service.ports,
        'protocols': service.protocols,
        'description': service.description,
    }
    return self._post('/service-objects', payload)

  def persist_policy(self, name: str, content: str,
                     description: Optional[str] = None,
                     status: str = 'draft') -> Dict[str, Any]:
    payload = {
        'name': name,
        'description': description,
        'content': content,
        'status': status,
    }
    return self._post('/policies', payload)

  def validate_policy(self, policy_id: int) -> Dict[str, Any]:
    return self._post(f'/policies/{policy_id}/validate', {})

  def persist_migration_output(
      self,
      policy_content: str,
      policy_name: str,
      network_objects: Optional[Dict[str, List[str]]] = None,
      service_objects: Optional[Dict[str, ServiceDef]] = None,
      description: Optional[str] = None,
      status: str = 'draft',
      validate: bool = True) -> Dict[str, Any]:
    """Persist migration artifacts to the Phase 2 API.

    Args:
      policy_content: Rendered Capirca policy text.
      policy_name: Name to use for the policy inside the API.
      network_objects: Extracted network objects keyed by name.
      service_objects: Extracted service objects keyed by name.
      description: Optional policy description.
      status: Policy status (default: draft).
      validate: Whether to immediately trigger validation after persistence.

    Returns:
      Dictionary containing persisted objects and validation response.
    """
    persisted_networks = []
    persisted_services = []

    for name, addresses in (network_objects or {}).items():
      persisted_networks.append(
          self.persist_network_object(name, addresses))

    for service in (service_objects or {}).values():
      persisted_services.append(self.persist_service_object(service))

    policy = self.persist_policy(policy_name, policy_content,
                                 description=description, status=status)

    validation = None
    if validate:
      validation = self.validate_policy(policy['id'])

    return {
        'policy': policy,
        'validation': validation,
        'network_objects': persisted_networks,
        'service_objects': persisted_services,
    }
