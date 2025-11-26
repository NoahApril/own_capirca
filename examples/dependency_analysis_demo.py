#!/usr/bin/env python3
"""Real data dependency analysis using Confluence API.

This script fetches a Confluence page and analyzes its dependencies
to identify:
- Unresolved references (missing definitions)
- Dependency chains
- Circular dependencies
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from capirca.utils import migration
from capirca.utils.confluence.confluence_http_service import ConfluenceService


def main():
    # Load environment variables from project root
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
    
    # Get page ID from user
    if len(sys.argv) > 1:
        page_id = sys.argv[1]
    else:
        page_id = input("Enter Confluence page ID: ").strip()
    
    if not page_id:
        print("Error: Page ID is required!")
        sys.exit(1)
    
    print("=" * 70)
    print("Confluence Dependency Analysis")
    print("=" * 70)
    print(f"Base URL: {base_url}")
    print(f"Page ID:  {page_id}")
    print("-" * 70)
    print()
    
    # Initialize Confluence service
    confluence = ConfluenceService(base_url, username, api_token)
    
    # Fetch page details
    print("Fetching page from Confluence...")
    page_data = confluence.fetch_page_details(page_id)
    
    if not page_data:
        print(f"Error: Failed to fetch page {page_id}")
        print("Please check:")
        print("  - Page ID is correct")
        print("  - API token has read permissions")
        print("  - Page is accessible")
        sys.exit(1)
    
    page_title = page_data.get('title', 'Unknown')
    print(f"✓ Fetched: {page_title}")
    print()
    
    # Extract HTML content
    if 'body' not in page_data or 'view' not in page_data['body']:
        print("Error: Page content not found!")
        print("The page might not contain any tables or content.")
        sys.exit(1)
    
    html_content = page_data['body']['view']['value']
    
    # Parse with ConfluenceParser
    print("Parsing tables...")
    parser = migration.ConfluenceParser()
    rules = parser.parse_html(html_content)
    
    print(f"✓ Parsed {len(rules)} firewall rules")
    print(f"✓ Found {len(parser.hosts)} hosts")
    print(f"✓ Found {len(parser.networks)} networks")
    print(f"✓ Found {len(parser.groups)} groups")
    print()
    
    # Analyze dependencies
    print("Analyzing dependencies...")
    analyzer = migration.DependencyAnalyzer()
    report = analyzer.analyze(parser)
    
    print("✓ Analysis complete")
    print()
    print("=" * 70)
    print(report.format_report())
    print("=" * 70)
    print()
    
    # Summary and recommendations
    if report.unresolved:
        print("⚠️  WARNINGS:")
        print(f"   - {len(report.unresolved)} unresolved reference(s)")
        print("   - You need to fetch additional pages:")
        for ref in sorted(report.unresolved):
            print(f"      • {ref}")
        print()
    
    if report.cycles:
        print("❌ ERRORS:")
        print(f"   - {len(report.cycles)} circular dependency(ies) detected")
        print("   - Fix these before proceeding!")
        print()
    
    if not report.unresolved and not report.cycles:
        print("✅ All checks passed!")
        print("   - No unresolved references")
        print("   - No circular dependencies")
        print("   - Safe to proceed with migration")
        print()
    
    # Save report to file
    report_filename = f"dependency_report_{page_id}.txt"
    with open(report_filename, 'w') as f:
        f.write(f"Confluence Page: {page_title} (ID: {page_id})\\n")
        f.write(f"URL: {base_url}/pages/viewpage.action?pageId={page_id}\\n\\n")
        f.write(report.format_report())
    
    print(f"📄 Report saved to: {report_filename}")


if __name__ == '__main__':
    main()
