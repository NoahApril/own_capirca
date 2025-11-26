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

"""Extended tests for capirca.utils.migration module supporting new data structures."""

from absl.testing import absltest
from capirca.utils import migration


class ConfluenceParserExtendedTest(absltest.TestCase):
  """Tests for ConfluenceParser with new data structures."""
  
  def setUp(self):
    super().setUp()
    self.parser = migration.ConfluenceParser()
    
    # Example data from user request
    self.hosts_html = """
    <table>
      <tr><th>FQDN</th><th>IP-Adresse</th><th>Funktion</th><th>Kommentar</th></tr>
      <tr><td>abc.xyz.de</td><td>10.79.122.12</td><td>Web-Frontende (Apache)</td><td>Web</td></tr>
      <tr><td>server.local</td><td>192.168.1.10</td><td>Backend</td><td>Internal</td></tr>
    </table>
    """
    
    self.networks_html = """
    <table>
      <tr><th>Name</th><th>IP-Adresse (CIDR)</th><th>Funktion</th><th>Kommentar</th></tr>
      <tr><td>Staff-Network</td><td>10.0.0.0/8</td><td>Mitarbeitende</td><td>siehe Well-Known-Names</td></tr>
      <tr><td>DMZ</td><td>172.16.0.0/12</td><td>DMZ Network</td><td></td></tr>
    </table>
    """
    
    self.groups_html = """
    <table>
      <tr><th>Name</th><th>Mitglieder (FQDN)</th><th>Funktion</th><th>Kommentar</th></tr>
      <tr><td>WS-Clients</td><td>Staff-Network, abc.xyz.de</td><td>Workstations</td><td></td></tr>
      <tr><td>All-Servers</td><td>server.local, DMZ</td><td>All Servers</td><td></td></tr>
    </table>
    """
    
    self.rules_html = """
    <table>
      <tr><th>Nummer</th><th>Quelle</th><th>Ziel</th><th>Ports/Protokolle</th><th>Sub-Rule/Firewall</th><th>Kommentar</th></tr>
      <tr><td>001</td><td>WS-Clients</td><td>All-Servers</td><td>80/tcp (HTTP) 443/tcp (HTTPS)</td><td></td><td>Web-Zugriff</td></tr>
    </table>
    """
    
    self.full_html = f"""
    <h2>Hosts</h2>
    {self.hosts_html}
    <h2>Networks</h2>
    {self.networks_html}
    <h2>Groups</h2>
    {self.groups_html}
    <h2>Rules</h2>
    {self.rules_html}
    """

  def testParseHosts(self):
    """Test parsing of Hosts table."""
    # Note: We expect the parser to handle this and return something we can inspect.
    # Since the current parser returns a list of FirewallRule, we might need to check 
    # if we can access the parsed objects directly or if we need to inspect the internal state.
    # For this test, we assume the parser will have a method or property to access parsed objects.
    # Or we might need to subclass/modify the parser to expose them.
    
    # For now, let's assume we can pass the HTML and it parses it into internal state.
    self.parser.parse_html(self.hosts_html)
    
    # We need to verify the hosts are parsed. 
    # Assuming we add a property 'hosts' to the parser or a result object.
    self.assertIn('abc.xyz.de', self.parser.hosts)
    self.assertEqual(self.parser.hosts['abc.xyz.de'], '10.79.122.12')

  def testParseNetworks(self):
    """Test parsing of Networks table."""
    self.parser.parse_html(self.networks_html)
    self.assertIn('Staff-Network', self.parser.networks)
    self.assertEqual(self.parser.networks['Staff-Network'], '10.0.0.0/8')

  def testParseGroups(self):
    """Test parsing of Groups table."""
    # We need hosts and networks defined for groups to make sense if we resolve them immediately.
    # Or we parse them as raw strings first.
    self.parser.parse_html(self.groups_html)
    self.assertIn('WS-Clients', self.parser.groups)
    self.assertIn('Staff-Network', self.parser.groups['WS-Clients'])
    self.assertIn('abc.xyz.de', self.parser.groups['WS-Clients'])

  def testFullResolution(self):
    """Test full parsing and resolution of rules."""
    rules = self.parser.parse_html(self.full_html)
    
    self.assertEqual(len(rules), 1)
    rule = rules[0]
    
    # Check if names are resolved to IPs/CIDRs in the rule
    # WS-Clients -> Staff-Network (10.0.0.0/8) + abc.xyz.de (10.79.122.12)
    expected_source = ['10.0.0.0/8', '10.79.122.12']
    # All-Servers -> server.local (192.168.1.10) + DMZ (172.16.0.0/12)
    expected_dest = ['192.168.1.10', '172.16.0.0/12']
    
    self.assertEqual(sorted(rule.source_addresses), sorted(expected_source))
    self.assertEqual(sorted(rule.destination_addresses), sorted(expected_dest))
    
    # Check ports
    # 80/tcp (HTTP) 443/tcp (HTTPS) -> ['80', '443'] and ['tcp']
    self.assertEqual(sorted(rule.destination_ports), ['443', '80'])
    self.assertEqual(rule.protocols, ['tcp'])

  def testComplexPorts(self):
    """Test parsing of complex port strings."""
    port_str = "80/tcp (HTTP) 443/tcp (HTTPS) 53/udp"
    ports, protocols = self.parser._parse_complex_ports(port_str)
    self.assertEqual(sorted(ports), ['443', '53', '80'])
    self.assertEqual(sorted(protocols), ['tcp', 'udp'])

if __name__ == '__main__':
  absltest.main()
