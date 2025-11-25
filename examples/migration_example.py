#!/usr/bin/env python3
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

"""Example usage of the Capirca migration utilities (Phase 1).

This script demonstrates the complete workflow for migrating firewall rules
from Confluence tables to Capirca policy format with automatic object extraction.

Usage:
    python examples/migration_example.py
"""

from capirca.utils import migration


def main():
  print("=" * 70)
  print("Capirca Migration Example - Phase 1: Data Migration Engine")
  print("=" * 70)
  print()
  
  sample_confluence_html = """
  <table>
    <tr>
      <th>Rule</th>
      <th>Source</th>
      <th>Destination</th>
      <th>Port</th>
      <th>Protocol</th>
      <th>Action</th>
      <th>Description</th>
    </tr>
    <tr>
      <td>allow-web-access</td>
      <td>10.0.0.0/8, 172.16.0.0/12</td>
      <td>192.168.1.10</td>
      <td>80, 443</td>
      <td>tcp</td>
      <td>allow</td>
      <td>Web server access from internal networks</td>
    </tr>
    <tr>
      <td>allow-ssh</td>
      <td>10.0.0.0/8, 172.16.0.0/12</td>
      <td>192.168.1.10</td>
      <td>22</td>
      <td>tcp</td>
      <td>allow</td>
      <td>SSH access for management</td>
    </tr>
    <tr>
      <td>allow-dns</td>
      <td>10.0.0.0/8</td>
      <td>8.8.8.8, 8.8.4.4</td>
      <td>53</td>
      <td>tcp, udp</td>
      <td>allow</td>
      <td>DNS queries to Google DNS</td>
    </tr>
    <tr>
      <td>deny-telnet</td>
      <td>any</td>
      <td>any</td>
      <td>23</td>
      <td>tcp</td>
      <td>deny</td>
      <td>Block insecure telnet protocol</td>
    </tr>
  </table>
  """
  
  print("Step 1: Parsing Confluence Table")
  print("-" * 70)
  parser = migration.ConfluenceParser()
  rules = parser.parse_table(sample_confluence_html)
  
  print(f"Parsed {len(rules)} rules from Confluence table:\n")
  for rule in rules:
    print(f"  - {rule.name}")
    print(f"    Source: {', '.join(rule.source_addresses) if rule.source_addresses else 'any'}")
    print(f"    Destination: {', '.join(rule.destination_addresses) if rule.destination_addresses else 'any'}")
    print(f"    Ports: {', '.join(rule.destination_ports) if rule.destination_ports else 'any'}")
    print(f"    Protocol: {', '.join(rule.protocols) if rule.protocols else 'any'}")
    print(f"    Action: {rule.action}")
    print()
  
  print("\nStep 2: Extracting Network Objects")
  print("-" * 70)
  extractor = migration.ObjectExtractor()
  network_objects = extractor.extract_network_objects(rules)
  
  print(f"Extracted {len(network_objects)} network objects:\n")
  for name, addresses in network_objects.items():
    print(f"  {name}:")
    for addr in addresses:
      print(f"    - {addr}")
    print()
  
  print("\nStep 3: Extracting Service Objects")
  print("-" * 70)
  service_objects = extractor.extract_service_objects(rules)
  
  print(f"Extracted {len(service_objects)} service objects:\n")
  for name, service_def in service_objects.items():
    print(f"  {name}:")
    print(f"    Ports: {', '.join(service_def.ports)}")
    print(f"    Protocols: {', '.join(service_def.protocols)}")
    print()
  
  print("\nStep 4: Generating Capirca Policy")
  print("-" * 70)
  generator = migration.CapircaGenerator(network_objects, service_objects)
  
  policy = generator.generate_policy(
    rules,
    policy_name='migrated-firewall-policy',
    targets=[
      ('cisco', 'migrated-filter'),
      ('juniper', 'migrated-filter'),
      ('iptables', 'INPUT DROP'),
    ],
    comment='Migrated from Confluence documentation\nGenerated automatically'
  )
  
  print("Generated Capirca Policy:\n")
  print(policy)
  
  print("\n" + "=" * 70)
  print("\nStep 5: Generating Network Definition File")
  print("-" * 70)
  network_defs = generator.generate_network_definitions()
  
  print("Network Definitions (.net file):\n")
  print(network_defs)
  
  print("\n" + "=" * 70)
  print("\nStep 6: Generating Service Definition File")
  print("-" * 70)
  service_defs = generator.generate_service_definitions()
  
  print("Service Definitions (.svc file):\n")
  print(service_defs)
  
  print("\n" + "=" * 70)
  print("\nMigration Complete!")
  print("=" * 70)
  print()
  print("Next Steps:")
  print("  1. Save the generated policy to a .pol file")
  print("  2. Save network definitions to NETWORK.net")
  print("  3. Save service definitions to SERVICES.svc")
  print("  4. Place files in appropriate def/ and policies/ directories")
  print("  5. Run: aclgen --definitions_directory=./def --policy_file=./policies/your.pol")
  print()
  
  
if __name__ == '__main__':
  main()
