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

"""Tests for capirca.utils.migration module."""

from absl.testing import absltest
from capirca.utils import migration


class FirewallRuleTest(absltest.TestCase):
  """Tests for FirewallRule dataclass."""
  
  def testBasicCreation(self):
    rule = migration.FirewallRule(name='test-rule')
    self.assertEqual(rule.name, 'test-rule')
    self.assertEqual(rule.action, 'accept')
    self.assertEqual(rule.source_addresses, [])
    
  def testFullCreation(self):
    rule = migration.FirewallRule(
      name='web-access',
      source_addresses=['10.0.0.0/8'],
      destination_addresses=['192.168.1.10'],
      destination_ports=['80', '443'],
      protocols=['tcp'],
      action='accept',
      comment='Web server access'
    )
    self.assertEqual(rule.name, 'web-access')
    self.assertEqual(rule.protocols, ['tcp'])
    self.assertEqual(rule.comment, 'Web server access')


class ConfluenceParserTest(absltest.TestCase):
  """Tests for ConfluenceParser class."""
  
  def setUp(self):
    super().setUp()
    self.parser = migration.ConfluenceParser()
    
  def testSimpleTable(self):
    html = """
    <table>
      <tr><th>Rule</th><th>Source</th><th>Destination</th><th>Port</th><th>Protocol</th><th>Action</th></tr>
      <tr><td>web-rule</td><td>10.0.0.0/8</td><td>192.168.1.10</td><td>80,443</td><td>tcp</td><td>allow</td></tr>
    </table>
    """
    rules = self.parser.parse_table(html)
    self.assertEqual(len(rules), 1)
    self.assertEqual(rules[0].name, 'web-rule')
    self.assertEqual(rules[0].source_addresses, ['10.0.0.0/8'])
    self.assertEqual(rules[0].destination_addresses, ['192.168.1.10'])
    self.assertEqual(rules[0].destination_ports, ['80', '443'])
    self.assertEqual(rules[0].protocols, ['tcp'])
    self.assertEqual(rules[0].action, 'accept')
    
  def testMultipleRules(self):
    html = """
    <table>
      <tr><th>Name</th><th>Source</th><th>Dest</th><th>Ports</th><th>Proto</th><th>Action</th></tr>
      <tr><td>rule1</td><td>10.0.0.0/8</td><td>192.168.1.10</td><td>80</td><td>tcp</td><td>permit</td></tr>
      <tr><td>rule2</td><td>172.16.0.0/12</td><td>192.168.1.20</td><td>443</td><td>tcp</td><td>deny</td></tr>
    </table>
    """
    rules = self.parser.parse_table(html)
    self.assertEqual(len(rules), 2)
    self.assertEqual(rules[0].name, 'rule1')
    self.assertEqual(rules[1].name, 'rule2')
    self.assertEqual(rules[1].action, 'deny')
    
  def testGermanHeaders(self):
    html = """
    <table>
      <tr><th>Regel</th><th>Source</th><th>Destination</th><th>Port</th><th>Protocol</th><th>Action</th><th>Beschreibung</th></tr>
      <tr><td>Test</td><td>10.0.0.0/8</td><td>192.168.1.10</td><td>22</td><td>tcp</td><td>allow</td><td>SSH Access</td></tr>
    </table>
    """
    rules = self.parser.parse_table(html)
    self.assertEqual(len(rules), 1)
    self.assertEqual(rules[0].comment, 'SSH Access')
    
  def testEmptyTable(self):
    html = """
    <table>
      <tr><th>Rule</th><th>Source</th><th>Destination</th></tr>
    </table>
    """
    rules = self.parser.parse_table(html)
    self.assertEqual(len(rules), 0)
    
  def testNoTable(self):
    html = "<div>No table here</div>"
    with self.assertRaises(migration.ParseError):
      self.parser.parse_table(html)
      
  def testActionNormalization(self):
    html = """
    <table>
      <tr><th>Rule</th><th>Source</th><th>Destination</th><th>Action</th></tr>
      <tr><td>r1</td><td>10.0.0.0/8</td><td>any</td><td>allow</td></tr>
      <tr><td>r2</td><td>10.0.0.0/8</td><td>any</td><td>permit</td></tr>
      <tr><td>r3</td><td>10.0.0.0/8</td><td>any</td><td>deny</td></tr>
      <tr><td>r4</td><td>10.0.0.0/8</td><td>any</td><td>drop</td></tr>
    </table>
    """
    rules = self.parser.parse_table(html)
    self.assertEqual(rules[0].action, 'accept')
    self.assertEqual(rules[1].action, 'accept')
    self.assertEqual(rules[2].action, 'deny')
    self.assertEqual(rules[3].action, 'deny')
    
  def testNameNormalization(self):
    html = """
    <table>
      <tr><th>Rule</th><th>Source</th><th>Destination</th></tr>
      <tr><td>Test Rule #1</td><td>10.0.0.0/8</td><td>any</td></tr>
      <tr><td>Allow Web (HTTP/HTTPS)</td><td>10.0.0.0/8</td><td>any</td></tr>
    </table>
    """
    rules = self.parser.parse_table(html)
    self.assertEqual(rules[0].name, 'test-rule-1')
    self.assertEqual(rules[1].name, 'allow-web-http-https')


class ObjectExtractorTest(absltest.TestCase):
  """Tests for ObjectExtractor class."""
  
  def setUp(self):
    super().setUp()
    self.extractor = migration.ObjectExtractor()
    
  def testExtractNetworkObjectsSimple(self):
    rules = [
      migration.FirewallRule(
        name='rule1',
        source_addresses=['10.0.0.0/8', '172.16.0.0/12'],
        destination_addresses=['192.168.1.10']
      ),
      migration.FirewallRule(
        name='rule2',
        source_addresses=['10.0.0.0/8', '172.16.0.0/12'],
        destination_addresses=['192.168.1.20']
      ),
    ]
    
    network_objects = self.extractor.extract_network_objects(rules)
    self.assertIn('NET_GROUP_2', network_objects)
    self.assertEqual(len(network_objects['NET_GROUP_2']), 2)
    
  def testExtractNetworkObjectsSingle(self):
    rules = [
      migration.FirewallRule(
        name='rule1',
        source_addresses=['10.0.0.0/8']
      ),
    ]
    
    network_objects = self.extractor.extract_network_objects(rules)
    self.assertEqual(len(network_objects), 0)
    
  def testExtractServiceObjects(self):
    rules = [
      migration.FirewallRule(
        name='rule1',
        destination_ports=['80', '443'],
        protocols=['tcp']
      ),
      migration.FirewallRule(
        name='rule2',
        destination_ports=['80', '443'],
        protocols=['tcp']
      ),
    ]
    
    service_objects = self.extractor.extract_service_objects(rules)
    self.assertEqual(len(service_objects), 1)
    service = list(service_objects.values())[0]
    self.assertEqual(service.ports, ['80', '443'])
    self.assertEqual(service.protocols, ['tcp'])
    
  def testExtractServiceObjectsNoMatch(self):
    rules = [
      migration.FirewallRule(
        name='rule1',
        destination_ports=['80'],
        protocols=['tcp']
      ),
      migration.FirewallRule(
        name='rule2',
        destination_ports=['443'],
        protocols=['tcp']
      ),
    ]
    
    service_objects = self.extractor.extract_service_objects(rules)
    self.assertEqual(len(service_objects), 0)
    
  def testNetworkNameGeneration(self):
    used_names = set()
    name1 = self.extractor._generate_network_name(['10.0.0.0/8'], used_names)
    self.assertIn('NET_', name1)
    
    used_names.add(name1)
    name2 = self.extractor._generate_network_name(['10.0.0.0/8'], used_names)
    self.assertNotEqual(name1, name2)
    
  def testServiceNameGeneration(self):
    used_names = set()
    name1 = self.extractor._generate_service_name(['80'], ['tcp'], used_names)
    self.assertEqual(name1, 'SVC_TCP_80')
    
    used_names.add(name1)
    name2 = self.extractor._generate_service_name(['80'], ['tcp'], used_names)
    self.assertEqual(name2, 'SVC_TCP_80_1')


class CapircaGeneratorTest(absltest.TestCase):
  """Tests for CapircaGenerator class."""
  
  def setUp(self):
    super().setUp()
    self.generator = migration.CapircaGenerator()
    
  def testGeneratePolicySimple(self):
    rules = [
      migration.FirewallRule(
        name='allow-web',
        source_addresses=['10.0.0.0/8'],
        destination_addresses=['192.168.1.10'],
        destination_ports=['80', '443'],
        protocols=['tcp'],
        action='accept',
        comment='Web access'
      ),
    ]
    
    policy = self.generator.generate_policy(rules, 'test-policy')
    self.assertIn('header {', policy)
    self.assertIn('target:: cisco test-policy', policy)
    self.assertIn('target:: juniper test-policy', policy)
    self.assertIn('term allow-web {', policy)
    self.assertIn('source-address:: 10.0.0.0/8', policy)
    self.assertIn('destination-address:: 192.168.1.10', policy)
    self.assertIn('destination-port:: 80 443', policy)
    self.assertIn('protocol:: tcp', policy)
    self.assertIn('action:: accept', policy)
    self.assertIn('comment:: "Web access"', policy)
    
  def testGeneratePolicyWithObjects(self):
    network_objects = {
      'INTERNAL_NET': ['10.0.0.0/8', '172.16.0.0/12'],
    }
    service_objects = {
      'WEB_SERVICES': migration.ServiceDef(
        name='WEB_SERVICES',
        ports=['80', '443'],
        protocols=['tcp']
      ),
    }
    
    generator = migration.CapircaGenerator(network_objects, service_objects)
    
    rules = [
      migration.FirewallRule(
        name='allow-web',
        source_addresses=['10.0.0.0/8', '172.16.0.0/12'],
        destination_addresses=['192.168.1.10'],
        destination_ports=['80', '443'],
        protocols=['tcp'],
        action='accept'
      ),
    ]
    
    policy = generator.generate_policy(rules, 'test-policy')
    self.assertIn('source-address:: INTERNAL_NET', policy)
    self.assertIn('destination-port:: WEB_SERVICES', policy)
    
  def testGeneratePolicyCustomTargets(self):
    rules = [
      migration.FirewallRule(
        name='test-rule',
        action='accept'
      ),
    ]
    
    targets = [
      ('cisco', 'my-filter'),
      ('juniper', 'my-filter'),
      ('iptables', 'INPUT DROP'),
    ]
    
    policy = self.generator.generate_policy(
      rules, 'test-policy', targets=targets
    )
    
    self.assertIn('target:: cisco my-filter', policy)
    self.assertIn('target:: juniper my-filter', policy)
    self.assertIn('target:: iptables INPUT DROP', policy)
    
  def testGeneratePolicyWithHeaderComment(self):
    rules = [
      migration.FirewallRule(name='test-rule', action='accept'),
    ]
    
    policy = self.generator.generate_policy(
      rules,
      'test-policy',
      comment='This is a test policy\nGenerated automatically'
    )
    
    self.assertIn('comment:: "This is a test policy"', policy)
    self.assertIn('comment:: "Generated automatically"', policy)
    
  def testGenerateNetworkDefinitions(self):
    network_objects = {
      'INTERNAL_NET': ['10.0.0.0/8', '172.16.0.0/12'],
      'DMZ_NET': ['192.168.1.0/24'],
    }
    
    generator = migration.CapircaGenerator(network_objects=network_objects)
    definitions = generator.generate_network_definitions()
    
    self.assertIn('INTERNAL_NET = 10.0.0.0/8', definitions)
    self.assertIn('172.16.0.0/12', definitions)
    self.assertIn('DMZ_NET = 192.168.1.0/24', definitions)
    
  def testGenerateServiceDefinitions(self):
    service_objects = {
      'WEB_SERVICES': migration.ServiceDef(
        name='WEB_SERVICES',
        ports=['80', '443'],
        protocols=['tcp']
      ),
      'DNS_SERVICES': migration.ServiceDef(
        name='DNS_SERVICES',
        ports=['53'],
        protocols=['tcp', 'udp']
      ),
    }
    
    generator = migration.CapircaGenerator(service_objects=service_objects)
    definitions = generator.generate_service_definitions()
    
    self.assertIn('WEB_SERVICES = 80/tcp', definitions)
    self.assertIn('443/tcp', definitions)
    self.assertIn('DNS_SERVICES = 53/tcp', definitions)
    self.assertIn('53/udp', definitions)
    
  def testGenerateTermWithOptions(self):
    rules = [
      migration.FirewallRule(
        name='established-rule',
        protocols=['tcp'],
        action='accept',
        options=['established']
      ),
    ]
    
    policy = self.generator.generate_policy(rules, 'test-policy')
    self.assertIn('option:: established', policy)


class IntegrationTest(absltest.TestCase):
  """Integration tests for complete migration workflow."""
  
  def testEndToEndWorkflow(self):
    html = """
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
        <td>web-access</td>
        <td>10.0.0.0/8</td>
        <td>192.168.1.10</td>
        <td>80,443</td>
        <td>tcp</td>
        <td>allow</td>
        <td>Web server access</td>
      </tr>
      <tr>
        <td>ssh-access</td>
        <td>10.0.0.0/8</td>
        <td>192.168.1.10</td>
        <td>22</td>
        <td>tcp</td>
        <td>allow</td>
        <td>SSH access</td>
      </tr>
    </table>
    """
    
    parser = migration.ConfluenceParser()
    rules = parser.parse_table(html)
    
    extractor = migration.ObjectExtractor()
    network_objects = extractor.extract_network_objects(rules)
    service_objects = extractor.extract_service_objects(rules)
    
    generator = migration.CapircaGenerator(network_objects, service_objects)
    policy = generator.generate_policy(
      rules,
      'migrated-policy',
      comment='Migrated from Confluence'
    )
    
    self.assertIn('header {', policy)
    self.assertIn('term web-access {', policy)
    self.assertIn('term ssh-access {', policy)
    self.assertIn('comment:: "Web server access"', policy)
    self.assertIn('comment:: "SSH access"', policy)
    
    net_defs = generator.generate_network_definitions()
    svc_defs = generator.generate_service_definitions()
    
    self.assertIsInstance(net_defs, str)
    self.assertIsInstance(svc_defs, str)


if __name__ == '__main__':
  absltest.main()
