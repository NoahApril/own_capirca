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

"""Tests for dependency analysis in migration module."""

from absl.testing import absltest
from capirca.utils import migration


class DependencyAnalyzerTest(absltest.TestCase):
  """Tests for DependencyAnalyzer class."""
  
  def setUp(self):
    super().setUp()
    self.analyzer = migration.DependencyAnalyzer()
    
  def testSimpleDefinitions(self):
    """Test simple case with no dependencies."""
    parser = migration.ConfluenceParser()
    parser.hosts = {'web.example.de': '10.0.0.1'}
    parser.networks = {'DMZ': '172.16.0.0/12'}
    parser.groups = {}
    
    report = self.analyzer.analyze(parser)
    
    self.assertEqual(len(report.definitions), 2)
    self.assertEqual(report.definitions['web.example.de'], 'host')
    self.assertEqual(report.definitions['DMZ'], 'network')
    self.assertEqual(len(report.references), 0)
    self.assertEqual(len(report.unresolved), 0)
    self.assertEqual(len(report.cycles), 0)
    self.assertEqual(report.max_depth, 0)
    
  def testGroupWithResolvedReferences(self):
    """Test group with resolved references."""
    parser = migration.ConfluenceParser()
    parser.hosts = {'web.server.de': '10.0.0.1'}
    parser.networks = {'Staff-Network': '10.1.0.0/16'}
    parser.groups = {
      'Server-Group': ['web.server.de', 'Staff-Network']
    }
    
    report = self.analyzer.analyze(parser)
    
    self.assertEqual(len(report.definitions), 3)
    self.assertIn('web.server.de', report.references)
    self.assertIn('Staff-Network', report.references)
    self.assertEqual(len(report.unresolved), 0)
    self.assertIn('Server-Group', report.dependency_chains)
    self.assertEqual(report.max_depth, 2)
    
  def testUnresolvedReference(self):
    """Test detection of unresolved references."""
    parser = migration.ConfluenceParser()
    parser.hosts = {}
    parser.networks = {'Staff-Network': '10.1.0.0/16'}
    parser.groups = {
      'WS-Clients': ['Staff-Network', 'Well-Known-Names']
    }
    
    report = self.analyzer.analyze(parser)
    
    self.assertIn('Well-Known-Names', report.unresolved)
    self.assertNotIn('Staff-Network', report.unresolved)
    self.assertEqual(len(report.unresolved), 1)
    
  def testNestedGroups(self):
    """Test nested group dependencies."""
    parser = migration.ConfluenceParser()
    parser.hosts = {'server.de': '10.0.0.1'}
    parser.networks = {'DMZ': '172.16.0.0/12'}
    parser.groups = {
      'Level1': ['server.de', 'DMZ'],
      'Level2': ['Level1'],
      'Level3': ['Level2']
    }
    
    report = self.analyzer.analyze(parser)
    
    self.assertEqual(len(report.definitions), 5)
    # Level3 depends on Level2, Level1, server.de, DMZ
    self.assertIn('Level3', report.dependency_chains)
    # Max depth should be 3 (Level3 -> Level2 -> Level1 -> actual resources)
    self.assertGreaterEqual(report.max_depth, 2)
    
  def testCycleDetection(self):
    """Test detection of circular dependencies."""
    parser = migration.ConfluenceParser()
    parser.hosts = {}
    parser.networks = {}
    parser.groups = {
      'Group-A': ['Group-B'],
      'Group-B': ['Group-A']
    }
    
    report = self.analyzer.analyze(parser)
    
    self.assertEqual(len(report.cycles), 1)
    cycle = report.cycles[0]
    self.assertIn('Group-A', cycle)
    self.assertIn('Group-B', cycle)
    
  def testComplexScenario(self):
    """Test complex scenario with multiple issues."""
    parser = migration.ConfluenceParser()
    parser.hosts = {
      'web1.example.de': '10.0.0.1',
      'web2.example.de': '10.0.0.2'
    }
    parser.networks = {
      'DMZ': '172.16.0.0/12',
      'Staff-Network': '10.1.0.0/16'
    }
    parser.groups = {
      'Web-Servers': ['web1.example.de', 'web2.example.de'],
      'All-Servers': ['Web-Servers', 'DMZ'],
      'WS-Clients': ['Staff-Network', 'Well-Known-Names'],  # Unresolved
      'Circular-A': ['Circular-B'],
      'Circular-B': ['Circular-A']
    }
    
    report = self.analyzer.analyze(parser)
    
    # Check definitions
    self.assertEqual(len(report.definitions), 9)
    
    # Check unresolved
    self.assertIn('Well-Known-Names', report.unresolved)
    self.assertEqual(len(report.unresolved), 1)
    
    # Check dependency chains
    self.assertIn('All-Servers', report.dependency_chains)
    
    # Check cycles
    self.assertEqual(len(report.cycles), 1)
    
  def testReportFormatting(self):
    """Test report formatting."""
    parser = migration.ConfluenceParser()
    parser.hosts = {'web.server.de': '10.0.0.1'}
    parser.networks = {'Staff-Network': '10.1.0.0/16'}
    parser.groups = {
      'Server-Group': ['web.server.de', 'Unknown-Network']
    }
    
    report = self.analyzer.analyze(parser)
    formatted = report.format_report()
    
    self.assertIn('Dependency Analysis Report', formatted)
    self.assertIn('Definitions', formatted)
    self.assertIn('Unresolved', formatted)
    self.assertIn('Unknown-Network', formatted)
    self.assertIn('web.server.de (host)', formatted)
    self.assertIn('Staff-Network (network)', formatted)
    
  def testIPAddressesSkipped(self):
    """Test that IP addresses are skipped in reference collection."""
    parser = migration.ConfluenceParser()
    parser.hosts = {}
    parser.networks = {}
    parser.groups = {
      'Mixed-Group': ['10.0.0.1', '192.168.1.0/24', 'Real-Reference']
    }
    
    report = self.analyzer.analyze(parser)
    
    # Only 'Real-Reference' should be in references, not IPs
    self.assertIn('Real-Reference', report.references)
    self.assertNotIn('10.0.0.1', report.references)
    self.assertNotIn('192.168.1.0/24', report.references)


if __name__ == '__main__':
  absltest.main()
