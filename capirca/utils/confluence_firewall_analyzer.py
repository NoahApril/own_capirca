#!/usr/bin/env python3
"""Confluence Firewall Analyzer - Analyze firewall configurations across Confluence pages.

This tool searches for Confluence pages with label 'dt=firewallregel', parses them,
and generates comprehensive reports about hosts, networks, groups, and dependencies.

Output:
  - Individual page dependency reports
  - Global overviews (hosts, networks, groups) in text and JSON
  - Unresolved references report
  - Statistics report
"""

import os
import sys
import json
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from capirca.utils import migration
from capirca.utils.confluence.confluence_http_service import ConfluenceService


@dataclass
class PageReference:
    """Reference to a Confluence page."""
    page_id: str
    page_title: str
    url: str


@dataclass
class HostInfo:
    """Aggregated host information."""
    fqdn: str
    ip_address: str
    source_pages: List[PageReference] = field(default_factory=list)
    function: str = ""
    comment: str = ""


@dataclass
class NetworkInfo:
    """Aggregated network information."""
    name: str
    cidr: str
    source_pages: List[PageReference] = field(default_factory=list)
    function: str = ""
    comment: str = ""


@dataclass
class GroupInfo:
    """Aggregated group information."""
    name: str
    members: List[str]
    source_pages: List[PageReference] = field(default_factory=list)
    function: str = ""
    comment: str = ""


@dataclass
class UnresolvedReference:
    """Unresolved reference information."""
    reference_name: str
    referenced_by_pages: List[Tuple[PageReference, str]] = field(default_factory=list)  # (page, context)


@dataclass
class Statistics:
    """Analysis statistics."""
    pages_analyzed: int = 0
    pages_failed: int = 0
    total_hosts: int = 0
    total_networks: int = 0
    total_groups: int = 0
    total_rules: int = 0
    duplicate_hosts: int = 0
    duplicate_networks: int = 0
    duplicate_groups: int = 0
    total_references: int = 0
    resolved_references: int = 0
    unresolved_references: int = 0
    circular_dependencies: int = 0
    max_dependency_depth: int = 0


class ConfluenceFirewallAnalyzer:
    """Analyze firewall configurations across multiple Confluence pages."""
    
    def __init__(self, confluence: ConfluenceService, base_url: str, output_dir: str = "output"):
        """Initialize analyzer.
        
        Args:
            confluence: ConfluenceService instance
            base_url: Confluence base URL for generating links
            output_dir: Output directory for reports
        """
        self.confluence = confluence
        self.base_url = base_url
        self.output_dir = output_dir
        self.analyzer = migration.DependencyAnalyzer()
        
        # Aggregated data
        self.all_hosts: Dict[str, HostInfo] = {}
        self.all_networks: Dict[str, NetworkInfo] = {}
        self.all_groups: Dict[str, GroupInfo] = {}
        self.unresolved_refs: Dict[str, UnresolvedReference] = {}
        self.page_reports: Dict[str, migration.DependencyReport] = {}
        self.statistics = Statistics()
        
    def run(self, label: str = "dt=firewallregel"):
        """Run complete analysis.
        
        Args:
            label: Confluence label to search for
        """
        # Create timestamp-based output directory
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        timestamped_output = os.path.join(self.output_dir, timestamp)
        self.output_dir = timestamped_output
        
        print("=" * 70)
        print("Confluence Firewall Analyzer")
        print("=" * 70)
        print(f"Label: {label}")
        print(f"Output: {self.output_dir}")
        print("-" * 70)
        print()
        
        # Create output directories
        self._create_output_dirs()
        
        # Step 1: Search for pages
        print("Step 1: Searching for pages...")
        pages = self._search_pages(label)
        print(f"✓ Found {len(pages)} pages")
        print()
        
        # Step 2: Process each page
        print("Step 2: Processing pages...")
        self._process_pages(pages)
        print(f"✓ Processed {self.statistics.pages_analyzed} pages successfully")
        if self.statistics.pages_failed > 0:
            print(f"⚠  Failed to process {self.statistics.pages_failed} pages")
        print()
        
        # Step 3: Global Resolution
        print("Step 3: Resolving references globally...")
        self._resolve_global_references()
        print(f"✓ Global resolution complete")
        print()
        
        # Step 4: Generate reports
        print("Step 4: Generating reports...")
        self._generate_all_reports()
        print("✓ All reports generated")
        print()
        
        print("=" * 70)
        print("Analysis Complete!")
        print(f"Output directory: {os.path.abspath(self.output_dir)}")
        print("=" * 70)
        
    def _create_output_dirs(self):
        """Create output directory structure."""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "page_reports"), exist_ok=True)
        
    def _search_pages(self, label: str) -> List[Dict]:
        """Search for pages with given label.
        
        Args:
            label: Confluence label
            
        Returns:
            List of page metadata
        """
        cql = f"label = '{label}'"
        results = []
        start = 0
        limit = 25
        
        while True:
            try:
                response = self.confluence.search_pages_by_cql(cql, start, limit)
                if 'results' in response:
                    results.extend(response['results'])
                    
                # Check if there are more results
                if 'next' not in response.get('_links', {}):
                    break
                start += limit
            except Exception as e:
                print(f"Error searching pages: {e}")
                break
                
        return results
        
    def _process_pages(self, pages: List[Dict]):
        """Process all pages.
        
        Args:
            pages: List of page metadata
        """
        for idx, page_meta in enumerate(pages, 1):
            page_id = page_meta['id']
            page_title = page_meta.get('title', 'Unknown')
            
            print(f"  [{idx}/{len(pages)}] Processing: {page_title} (ID: {page_id})")
            
            try:
                self._process_single_page(page_id, page_title)
                self.statistics.pages_analyzed += 1
            except Exception as e:
                print(f"      ✗ Error: {e}")
                self.statistics.pages_failed += 1
                
    def _process_single_page(self, page_id: str, page_title: str):
        """Process a single page.
        
        Args:
            page_id: Page ID
            page_title: Page title
        """
        # Fetch page
        page_data = self.confluence.fetch_page_details(page_id)
        if not page_data or 'body' not in page_data or 'view' not in page_data['body']:
            raise ValueError("Could not fetch page content")
            
        # Parse HTML
        html_content = page_data['body']['view']['value']
        parser = migration.ConfluenceParser()
        rules = parser.parse_html(html_content)
        
        # Check if page has any definitions - skip if empty
        has_definitions = (
            len(parser.hosts) > 0 or
            len(parser.networks) > 0 or
            len(parser.groups) > 0
        )

        if not has_definitions:
            print(f"      ⊘ Skipped: No definitions (hosts/networks/groups) found")
            raise ValueError("No definitions found - page ignored")

        # Analyze dependencies
        report = self.analyzer.analyze(parser)
        self.page_reports[page_id] = report
        
        # Create page reference
        page_ref = PageReference(
            page_id=page_id,
            page_title=page_title,
            url=f"{self.base_url}/pages/viewpage.action?pageId={page_id}"
        )
        
        # Aggregate data
        self._aggregate_hosts(parser, page_ref)
        self._aggregate_networks(parser, page_ref)
        self._aggregate_groups(parser, page_ref)
        self._aggregate_unresolved(report, page_ref)
        
        # Update statistics
        self.statistics.total_rules += len(rules)
        self.statistics.max_dependency_depth = max(
            self.statistics.max_dependency_depth,
            report.max_depth
        )
        self.statistics.circular_dependencies += len(report.cycles)
        
    def _aggregate_hosts(self, parser: migration.ConfluenceParser, page_ref: PageReference):
        """Aggregate host data.
        
        Args:
            parser: ConfluenceParser instance
            page_ref: Page reference
        """
        for fqdn, ip in parser.hosts.items():
            if fqdn in self.all_hosts:
                # Duplicate - add page reference
                self.all_hosts[fqdn].source_pages.append(page_ref)
                self.statistics.duplicate_hosts += 1
            else:
                self.all_hosts[fqdn] = HostInfo(
                    fqdn=fqdn,
                    ip_address=ip,
                    source_pages=[page_ref]
                )
                
        self.statistics.total_hosts = len(self.all_hosts)
        
    def _aggregate_networks(self, parser: migration.ConfluenceParser, page_ref: PageReference):
        """Aggregate network data.
        
        Args:
            parser: ConfluenceParser instance
            page_ref: Page reference
        """
        for name, cidr in parser.networks.items():
            if name in self.all_networks:
                # Duplicate - add page reference
                self.all_networks[name].source_pages.append(page_ref)
                self.statistics.duplicate_networks += 1
            else:
                self.all_networks[name] = NetworkInfo(
                    name=name,
                    cidr=cidr,
                    source_pages=[page_ref]
                )
                
        self.statistics.total_networks = len(self.all_networks)
        
    def _aggregate_groups(self, parser: migration.ConfluenceParser, page_ref: PageReference):
        """Aggregate group data.
        
        Args:
            parser: ConfluenceParser instance
            page_ref: Page reference
        """
        for name, members in parser.groups.items():
            if name in self.all_groups:
                # Duplicate - add page reference
                self.all_groups[name].source_pages.append(page_ref)
                self.statistics.duplicate_groups += 1
            else:
                self.all_groups[name] = GroupInfo(
                    name=name,
                    members=members,
                    source_pages=[page_ref]
                )
                
        self.statistics.total_groups = len(self.all_groups)
        
    def _aggregate_unresolved(self, report: migration.DependencyReport, page_ref: PageReference):
        """Aggregate unresolved references.
        
        Args:
            report: DependencyReport
            page_ref: Page reference
        """
        for ref in report.unresolved:
            if ref not in self.unresolved_refs:
                self.unresolved_refs[ref] = UnresolvedReference(reference_name=ref)
                
            # Find which group references this
            context = "Unknown context"
            for group_name, chain in report.dependency_chains.items():
                if ref in chain:
                    context = f"In Group: {group_name}"
                    break
                    
            self.unresolved_refs[ref].referenced_by_pages.append((page_ref, context))
            
        # Update statistics (initial local count)
        self.statistics.total_references += len(report.references)
        # resolved_references and unresolved_references will be recalculated globally
        
    def _resolve_global_references(self):
        """Resolve references against global definitions."""
        resolved_count = 0
        refs_to_remove = []
        
        for ref_name in self.unresolved_refs:
            # Check if defined anywhere
            is_defined = (
                ref_name in self.all_hosts or
                ref_name in self.all_networks or
                ref_name in self.all_groups
            )
            
            if is_defined:
                refs_to_remove.append(ref_name)
                resolved_count += 1
                
        # Remove resolved references
        for ref_name in refs_to_remove:
            del self.unresolved_refs[ref_name]
            
        print(f"  ✓ Resolved {resolved_count} references using global definitions")
        
        # Update statistics
        self.statistics.unresolved_references = len(self.unresolved_refs)
        self.statistics.resolved_references = self.statistics.total_references - self.statistics.unresolved_references

    def _generate_all_reports(self):
        """Generate all reports."""
        self._generate_page_reports()
        self._generate_hosts_overview()
        self._generate_networks_overview()
        self._generate_groups_overview()
        self._generate_unresolved_report()
        self._generate_statistics_report()
        self._generate_markdown_overview()  # Generates OVERVIEW.html

    def _generate_page_reports(self):
        """Generate individual page dependency reports."""
        for page_id, report in self.page_reports.items():
            # Find page title
            page_title = "Unknown"
            for ref in (list(self.all_hosts.values()) + 
                       list(self.all_networks.values()) + 
                       list(self.all_groups.values())):
                for page_ref in ref.source_pages:
                    if page_ref.page_id == page_id:
                        page_title = page_ref.page_title
                        break
                        
            # Sanitize filename
            safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' 
                               for c in page_title)
            filename = f"page_{page_id}_{safe_title}.txt"
            filepath = os.path.join(self.output_dir, "page_reports", filename)
            
            with open(filepath, 'w') as f:
                f.write(f"Confluence Page: {page_title} (ID: {page_id})\n")
                f.write(f"URL: {self.base_url}/pages/viewpage.action?pageId={page_id}\n\n")
                f.write(report.format_report())
                
    def _generate_hosts_overview(self):
        """Generate hosts overview in text and JSON."""
        # Text format
        filepath_txt = os.path.join(self.output_dir, "hosts_overview.txt")
        with open(filepath_txt, 'w') as f:
            f.write(f"Hosts Overview (Total: {len(self.all_hosts)})\n")
            f.write("=" * 70 + "\n\n")
            
            for fqdn in sorted(self.all_hosts.keys()):
                host = self.all_hosts[fqdn]
                f.write(f"{fqdn}\n")
                f.write(f"  IP: {host.ip_address}\n")
                f.write(f"  Defined in:\n")
                for page_ref in host.source_pages:
                    f.write(f"    - Page: {page_ref.page_title} (ID: {page_ref.page_id})\n")
                    f.write(f"      URL: {page_ref.url}\n")
                f.write("\n")
                
        # JSON format
        filepath_json = os.path.join(self.output_dir, "hosts_overview.json")
        hosts_dict = {}
        for fqdn, host in self.all_hosts.items():
            hosts_dict[fqdn] = {
                "ip_address": host.ip_address,
                "source_pages": [
                    {
                        "page_id": ref.page_id,
                        "page_title": ref.page_title,
                        "url": ref.url
                    }
                    for ref in host.source_pages
                ]
            }
            
        with open(filepath_json, 'w') as f:
            json.dump(hosts_dict, f, indent=2)
            
    def _generate_networks_overview(self):
        """Generate networks overview in text and JSON."""
        # Text format
        filepath_txt = os.path.join(self.output_dir, "networks_overview.txt")
        with open(filepath_txt, 'w') as f:
            f.write(f"Networks Overview (Total: {len(self.all_networks)})\n")
            f.write("=" * 70 + "\n\n")
            
            for name in sorted(self.all_networks.keys()):
                network = self.all_networks[name]
                f.write(f"{name}\n")
                f.write(f"  CIDR: {network.cidr}\n")
                f.write(f"  Defined in:\n")
                for page_ref in network.source_pages:
                    f.write(f"    - Page: {page_ref.page_title} (ID: {page_ref.page_id})\n")
                    f.write(f"      URL: {page_ref.url}\n")
                f.write("\n")
                
        # JSON format
        filepath_json = os.path.join(self.output_dir, "networks_overview.json")
        networks_dict = {}
        for name, network in self.all_networks.items():
            networks_dict[name] = {
                "cidr": network.cidr,
                "source_pages": [
                    {
                        "page_id": ref.page_id,
                        "page_title": ref.page_title,
                        "url": ref.url
                    }
                    for ref in network.source_pages
                ]
            }
            
        with open(filepath_json, 'w') as f:
            json.dump(networks_dict, f, indent=2)
            
    def _generate_groups_overview(self):
        """Generate groups overview in text and JSON."""
        # Text format
        filepath_txt = os.path.join(self.output_dir, "groups_overview.txt")
        with open(filepath_txt, 'w') as f:
            f.write(f"Groups Overview (Total: {len(self.all_groups)})\n")
            f.write("=" * 70 + "\n\n")
            
            for name in sorted(self.all_groups.keys()):
                group = self.all_groups[name]
                f.write(f"{name}\n")
                f.write(f"  Members: {', '.join(group.members)}\n")
                f.write(f"  Defined in:\n")
                for page_ref in group.source_pages:
                    f.write(f"    - Page: {page_ref.page_title} (ID: {page_ref.page_id})\n")
                    f.write(f"      URL: {page_ref.url}\n")
                f.write("\n")
                
        # JSON format
        filepath_json = os.path.join(self.output_dir, "groups_overview.json")
        groups_dict = {}
        for name, group in self.all_groups.items():
            groups_dict[name] = {
                "members": group.members,
                "source_pages": [
                    {
                        "page_id": ref.page_id,
                        "page_title": ref.page_title,
                        "url": ref.url
                    }
                    for ref in group.source_pages
                ]
            }
            
        with open(filepath_json, 'w') as f:
            json.dump(groups_dict, f, indent=2)
            
    def _generate_unresolved_report(self):
        """Generate unresolved references report."""
        filepath = os.path.join(self.output_dir, "unresolved_references.txt")
        with open(filepath, 'w') as f:
            f.write(f"Unresolved References (Total: {len(self.unresolved_refs)})\n")
            f.write("=" * 70 + "\n\n")
            
            for ref_name in sorted(self.unresolved_refs.keys()):
                unresolved = self.unresolved_refs[ref_name]
                f.write(f"{ref_name}\n")
                f.write(f"  Referenced by:\n")
                for page_ref, context in unresolved.referenced_by_pages:
                    f.write(f"    - Page: {page_ref.page_title} (ID: {page_ref.page_id})\n")
                    f.write(f"      URL: {page_ref.url}\n")
                    f.write(f"      {context}\n")
                f.write("\n")
                
    def _generate_statistics_report(self):
        """Generate statistics report."""
        filepath = os.path.join(self.output_dir, "statistics_report.txt")
        with open(filepath, 'w') as f:
            f.write("Statistics Report\n")
            f.write("=" * 70 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"Pages Analyzed: {self.statistics.pages_analyzed}\n")
            if self.statistics.pages_failed > 0:
                f.write(f"Pages Failed: {self.statistics.pages_failed}\n")
            f.write("\n")
            
            f.write("Total Definitions:\n")
            f.write(f"  - Hosts: {self.statistics.total_hosts}\n")
            f.write(f"  - Networks: {self.statistics.total_networks}\n")
            f.write(f"  - Groups: {self.statistics.total_groups}\n")
            f.write(f"  - Firewall Rules: {self.statistics.total_rules}\n")
            f.write("\n")
            
            if (self.statistics.duplicate_hosts > 0 or 
                self.statistics.duplicate_networks > 0 or 
                self.statistics.duplicate_groups > 0):
                f.write("Duplicates:\n")
                f.write(f"  - Hosts defined in multiple pages: {self.statistics.duplicate_hosts}\n")
                f.write(f"  - Networks defined in multiple pages: {self.statistics.duplicate_networks}\n")
                f.write(f"  - Groups defined in multiple pages: {self.statistics.duplicate_groups}\n")
                f.write("\n")
                
            f.write("Dependency Analysis:\n")
            f.write(f"  - Total References: {self.statistics.total_references}\n")
            f.write(f"  - Resolved: {self.statistics.resolved_references} ")
            if self.statistics.total_references > 0:
                pct = (self.statistics.resolved_references / self.statistics.total_references) * 100
                f.write(f"({pct:.1f}%)")
            f.write("\n")
            f.write(f"  - Unresolved: {self.statistics.unresolved_references} ")
            if self.statistics.total_references > 0:
                pct = (self.statistics.unresolved_references / self.statistics.total_references) * 100
                f.write(f"({pct:.1f}%)")
            f.write("\n")
            f.write(f"  - Circular Dependencies: {self.statistics.circular_dependencies}\n")
            f.write("\n")
            
            f.write(f"Max Dependency Depth: {self.statistics.max_dependency_depth}\n")

    def _generate_markdown_overview(self):
        """Generate comprehensive HTML overview with tables."""
        filepath = os.path.join(self.output_dir, "OVERVIEW.html")

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Firewall Configuration Overview</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .timestamp {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .summary-item {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }}
        
        .summary-item:hover {{
            background: #f0f1ff;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
        }}
        
        .summary-item .label {{
            font-size: 0.85em;
            color: #666;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 8px;
        }}
        
        .summary-item .value {{
            font-size: 1.8em;
            color: #667eea;
            font-weight: bold;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            color: #667eea;
            font-size: 1.5em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        thead {{
            background: #f8f9fa;
        }}
        
        th {{
            text-align: left;
            padding: 12px 15px;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #e0e0e0;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        tbody tr:hover {{
            background: #f8f9fa;
        }}
        
        td code {{
            background: #f0f1ff;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #667eea;
        }}
        
        td a {{
            color: #667eea;
            text-decoration: none;
            transition: all 0.2s;
            word-break: break-word;
        }}
        
        td a:hover {{
            text-decoration: underline;
            color: #764ba2;
        }}
        
        .empty-message {{
            text-align: center;
            padding: 30px;
            color: #999;
            font-style: italic;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        
        .members {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}
        
        .member-badge {{
            background: #e8ecff;
            color: #667eea;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        
        .occurrences {{
            background: #667eea;
            color: white;
            padding: 4px 10px;
            border-radius: 4px;
            font-weight: 600;
            text-align: center;
            display: inline-block;
            min-width: 40px;
        }}
        
        .search-container {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 30px;
            border: 2px solid #e0e0e0;
        }}
        
        .search-box {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }}
        
        .search-input {{
            flex: 1;
            min-width: 200px;
            padding: 10px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 1em;
            transition: all 0.3s ease;
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 8px rgba(102, 126, 234, 0.3);
        }}
        
        .search-button {{
            padding: 10px 25px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .search-button:hover {{
            background: #764ba2;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }}
        
        .reset-button {{
            padding: 10px 25px;
            background: #999;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .reset-button:hover {{
            background: #666;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(100, 100, 100, 0.3);
        }}
        
        .results-info {{
            font-size: 0.9em;
            color: #666;
            margin-top: 10px;
            padding: 10px;
            background: white;
            border-radius: 6px;
            border-left: 3px solid #667eea;
        }}
        
        .hidden-row {{
            display: none !important;
        }}
        
        .highlighted {{
            background: #fff3cd;
            font-weight: 600;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px 40px;
            text-align: center;
            color: #999;
            font-size: 0.85em;
        }}
    </style>
    <script>
        let currentSearchTerm = '';
        let currentTable = null;
        
        function initSearch() {{
            const searchInput = document.getElementById('globalSearch');
            const hostsBtn = document.getElementById('searchHostsBtn');
            const networksBtn = document.getElementById('searchNetworksBtn');
            const groupsBtn = document.getElementById('searchGroupsBtn');
            const resetBtn = document.getElementById('resetSearchBtn');
            
            if (searchInput) searchInput.addEventListener('input', handleSearch);
            if (hostsBtn) hostsBtn.addEventListener('click', () => searchTable('hosts'));
            if (networksBtn) networksBtn.addEventListener('click', () => searchTable('networks'));
            if (groupsBtn) groupsBtn.addEventListener('click', () => searchTable('groups'));
            if (resetBtn) resetBtn.addEventListener('click', resetSearch);
            
            // Allow Enter key to trigger search
            if (searchInput) {{
                searchInput.addEventListener('keypress', (e) => {{
                    if (e.key === 'Enter') handleSearch();
                }});
            }}
        }}
        
        function handleSearch() {{
            const searchInput = document.getElementById('globalSearch');
            currentSearchTerm = searchInput.value.toLowerCase();
            
            if (!currentSearchTerm.trim()) {{
                resetSearch();
                return;
            }}
            
            // Search in all tables
            searchTableRows('hostsTable');
            searchTableRows('networksTable');
            searchTableRows('groupsTable');
            updateResultsInfo();
        }}
        
        function searchTable(tableType) {{
            currentSearchTerm = document.getElementById('globalSearch').value.toLowerCase();
            if (!currentSearchTerm.trim()) {{
                resetSearch();
                return;
            }}
            
            if (tableType === 'hosts') {{
                searchTableRows('hostsTable');
            }} else if (tableType === 'networks') {{
                searchTableRows('networksTable');
            }} else if (tableType === 'groups') {{
                searchTableRows('groupsTable');
            }}
            
            updateResultsInfo();
        }}
        
        function searchTableRows(tableId) {{
            const table = document.getElementById(tableId);
            if (!table) return;
            
            const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
            let visibleCount = 0;
            
            for (let row of rows) {{
                const text = row.textContent.toLowerCase();
                const matches = text.includes(currentSearchTerm);
                
                if (matches) {{
                    row.classList.remove('hidden-row');
                    visibleCount++;
                }} else {{
                    row.classList.add('hidden-row');
                }}
            }}
        }}
        
        function resetSearch() {{
            const searchInput = document.getElementById('globalSearch');
            searchInput.value = '';
            currentSearchTerm = '';
            
            // Show all rows
            document.querySelectorAll('tbody tr').forEach(row => {{
                row.classList.remove('hidden-row', 'highlighted');
            }});
            
            updateResultsInfo();
        }}
        
        function updateResultsInfo() {{
            const hostsTable = document.getElementById('hostsTable');
            const networksTable = document.getElementById('networksTable');
            const groupsTable = document.getElementById('groupsTable');
            
            let totalRows = 0;
            let visibleRows = 0;
            
            [hostsTable, networksTable, groupsTable].forEach(table => {{
                if (table) {{
                    const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
                    totalRows += rows.length;
                    visibleRows += Array.from(rows).filter(r => !r.classList.contains('hidden-row')).length;
                }}
            }});
            
            const infoDiv = document.getElementById('resultsInfo');
            if (infoDiv) {{
                if (currentSearchTerm) {{
                    infoDiv.innerHTML = `<strong>Results:</strong> Showing ${{visibleRows}} of ${{totalRows}} entries matching "${{currentSearchTerm}}"`;
                    infoDiv.style.display = 'block';
                }} else {{
                    infoDiv.innerHTML = '';
                    infoDiv.style.display = 'none';
                }}
            }}
        }}
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', initSearch);
    </script>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Firewall Configuration Overview</h1>
            <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        
        <div class="content">
            <!-- Search Section -->
            <div class="search-container">
                <div class="search-box">
                    <input type="text" id="globalSearch" class="search-input" placeholder="🔍 Search hosts, networks, groups, IPs, CIDRs...">
                    <button class="search-button" onclick="handleSearch()">Search</button>
                    <button class="reset-button" onclick="resetSearch()">Reset</button>
                </div>
                <div id="resultsInfo" class="results-info" style="display: none;"></div>
            </div>
            
            <!-- Summary Section -->
            <div class="summary">
                <div class="summary-item">
                    <div class="label">Pages Analyzed</div>
                    <div class="value">{self.statistics.pages_analyzed}</div>
                </div>
                <div class="summary-item">
                    <div class="label">Total Hosts</div>
                    <div class="value">{self.statistics.total_hosts}</div>
                </div>
                <div class="summary-item">
                    <div class="label">Total Networks</div>
                    <div class="value">{self.statistics.total_networks}</div>
                </div>
                <div class="summary-item">
                    <div class="label">Total Groups</div>
                    <div class="value">{self.statistics.total_groups}</div>
                </div>
                <div class="summary-item">
                    <div class="label">Firewall Rules</div>
                    <div class="value">{self.statistics.total_rules}</div>
                </div>
                <div class="summary-item">
                    <div class="label">Unresolved Refs</div>
                    <div class="value">{self.statistics.unresolved_references}</div>
                </div>
            </div>
            
            <!-- Hosts Section -->
            <div class="section">
                <h2>👥 Hosts</h2>
                {self._generate_hosts_table_html()}
            </div>
            
            <!-- Networks Section -->
            <div class="section">
                <h2>🌐 Networks</h2>
                {self._generate_networks_table_html()}
            </div>
            
            <!-- Groups Section -->
            <div class="section">
                <h2>👫 Groups</h2>
                {self._generate_groups_table_html()}
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by Confluence Firewall Analyzer</p>
        </div>
    </div>
</body>
</html>"""

        with open(filepath, 'w') as f:
            f.write(html_content)

    def _generate_hosts_table_html(self) -> str:
        """Generate HTML table for hosts."""
        if not self.all_hosts:
            return '<div class="empty-message">No hosts defined</div>'

        html = '<table id="hostsTable"><thead><tr><th>FQDN</th><th>IP Address</th><th>Source Pages</th><th>Occurrences</th></tr></thead><tbody>'

        for fqdn in sorted(self.all_hosts.keys()):
            host = self.all_hosts[fqdn]
            pages_html = ", ".join([f'<a href="{ref.url}" target="_blank">{ref.page_title}</a>'
                                   for ref in host.source_pages])
            occurrences = len(host.source_pages)
            html += f'<tr><td><code>{fqdn}</code></td><td><code>{host.ip_address}</code></td><td>{pages_html}</td><td><span class="occurrences">{occurrences}</span></td></tr>'

        html += '</tbody></table>'
        return html

    def _generate_networks_table_html(self) -> str:
        """Generate HTML table for networks."""
        if not self.all_networks:
            return '<div class="empty-message">No networks defined</div>'

        html = '<table id="networksTable"><thead><tr><th>Network Name</th><th>CIDR</th><th>Source Pages</th><th>Occurrences</th></tr></thead><tbody>'

        for name in sorted(self.all_networks.keys()):
            network = self.all_networks[name]
            pages_html = ", ".join([f'<a href="{ref.url}" target="_blank">{ref.page_title}</a>'
                                   for ref in network.source_pages])
            occurrences = len(network.source_pages)
            html += f'<tr><td><code>{name}</code></td><td><code>{network.cidr}</code></td><td>{pages_html}</td><td><span class="occurrences">{occurrences}</span></td></tr>'

        html += '</tbody></table>'
        return html

    def _generate_groups_table_html(self) -> str:
        """Generate HTML table for groups."""
        if not self.all_groups:
            return '<div class="empty-message">No groups defined</div>'

        html = '<table id="groupsTable"><thead><tr><th>Group Name</th><th>Members</th><th>Source Pages</th><th>Occurrences</th></tr></thead><tbody>'

        for name in sorted(self.all_groups.keys()):
            group = self.all_groups[name]
            members_html = '<div class="members">' + "".join([f'<span class="member-badge">{member}</span>'
                                                             for member in group.members]) + '</div>'
            pages_html = ", ".join([f'<a href="{ref.url}" target="_blank">{ref.page_title}</a>'
                                   for ref in group.source_pages])
            occurrences = len(group.source_pages)
            html += f'<tr><td><code>{name}</code></td><td>{members_html}</td><td>{pages_html}</td><td><span class="occurrences">{occurrences}</span></td></tr>'

        html += '</tbody></table>'
        return html


def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()
    
    base_url = os.getenv('CONFLUENCE_URL')
    api_token = os.getenv('CONFLUENCE_API_TOKEN')
    username = os.getenv('CONFLUENCE_USERNAME')
    
    if not all([base_url, api_token, username]):
        print("Error: Missing environment variables!")
        print("Please create a .env file with:")
        print("  CONFLUENCE_URL=https://your-confluence-instance.com")
        print("  CONFLUENCE_API_TOKEN=your_api_token")
        print("  CONFLUENCE_USERNAME=your_email@example.com")
        sys.exit(1)
        
    # Initialize Confluence service
    confluence = ConfluenceService(base_url, username, api_token)
    
    # Run analyzer
    analyzer = ConfluenceFirewallAnalyzer(confluence, base_url)
    analyzer.run()


if __name__ == '__main__':
    main()
