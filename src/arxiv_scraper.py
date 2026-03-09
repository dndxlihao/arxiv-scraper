#!/usr/bin/env python3
"""
arXiv Paper Scraper

A simple script to fetch papers from arXiv based on search queries.
Supports multiple search terms, date ranges, and output formats.

Usage:
    python arxiv_scraper.py --query "machine learning" --max-results 10
    python arxiv_scraper.py --query "quantum computing" --start-date 2025-01-01 --output json
"""

import argparse
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import json
import time
from typing import List, Dict, Optional
import sys


class ArxivScraper:
    """Scrape papers from arXiv API."""
    
    BASE_URL = "http://export.arxiv.org/api/query"
    
    def __init__(self, max_results: int = 10, delay: float = 3.0):
        """
        Initialize the scraper.
        
        Args:
            max_results: Maximum number of results to fetch per query
            delay: Delay between requests to avoid rate limiting (seconds)
        """
        self.max_results = max_results
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'arXiv-Scraper/1.0 (contact: your-email@example.com)'
        })
    
    def search(
        self,
        query: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category: Optional[str] = None,
        sort_by: str = "submittedDate",
        sort_order: str = "descending"
    ) -> List[Dict]:
        """
        Search for papers on arXiv.
        
        Args:
            query: Search query string
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            category: arXiv category (e.g., cs.AI, cs.LG, quant-ph)
            sort_by: Field to sort by ("relevance", "lastUpdatedDate", "submittedDate")
            sort_order: "ascending" or "descending"
            
        Returns:
            List of paper dictionaries
        """
        # Build search parameters
        search_query = query
        
        # Add category if specified
        if category:
            search_query = f"cat:{category} AND ({search_query})"
        
        # Add date range if specified
        if start_date:
            search_query = f"submittedDate:[{start_date} TO {end_date or datetime.now().strftime('%Y-%m-%d')}] AND ({search_query})"
        
        params = {
            'search_query': search_query,
            'start': 0,
            'max_results': self.max_results,
            'sortBy': sort_by,
            'sortOrder': sort_order
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
            
            # Parse XML response
            papers = self._parse_xml_response(response.text)
            
            # Respect rate limiting
            time.sleep(self.delay)
            
            return papers
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from arXiv: {e}", file=sys.stderr)
            return []
        except ET.ParseError as e:
            print(f"Error parsing XML response: {e}", file=sys.stderr)
            return []
    
    def _parse_xml_response(self, xml_content: str) -> List[Dict]:
        """Parse arXiv API XML response."""
        root = ET.fromstring(xml_content)
        
        # Define XML namespaces
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        
        papers = []
        
        for entry in root.findall('atom:entry', ns):
            paper = {}
            
            # Extract basic information
            paper['id'] = entry.find('atom:id', ns).text if entry.find('atom:id', ns) is not None else None
            paper['title'] = entry.find('atom:title', ns).text.strip() if entry.find('atom:title', ns) is not None else None
            paper['summary'] = entry.find('atom:summary', ns).text.strip() if entry.find('atom:summary', ns) is not None else None
            
            # Extract authors
            authors = []
            for author in entry.findall('atom:author', ns):
                name = author.find('atom:name', ns)
                if name is not None:
                    authors.append(name.text)
            paper['authors'] = authors
            
            # Extract categories
            categories = []
            for category in entry.findall('atom:category', ns):
                term = category.get('term')
                if term:
                    categories.append(term)
            paper['categories'] = categories
            
            # Extract links
            links = []
            for link in entry.findall('atom:link', ns):
                link_info = {
                    'href': link.get('href'),
                    'rel': link.get('rel', ''),
                    'title': link.get('title', '')
                }
                links.append(link_info)
            paper['links'] = links
            
            # Extract published and updated dates
            published = entry.find('atom:published', ns)
            updated = entry.find('atom:updated', ns)
            paper['published'] = published.text if published is not None else None
            paper['updated'] = updated.text if updated is not None else None
            
            # Extract arXiv identifier
            arxiv_id = paper['id'].split('/')[-1] if paper['id'] else None
            paper['arxiv_id'] = arxiv_id
            
            papers.append(paper)
        
        return papers
    
    def save_to_file(self, papers: List[Dict], output_format: str = 'json', filename: Optional[str] = None):
        """
        Save papers to a file.
        
        Args:
            papers: List of paper dictionaries
            output_format: 'json', 'txt', or 'csv'
            filename: Output filename (optional)
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"arxiv_papers_{timestamp}.{output_format}"
        
        try:
            if output_format == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(papers, f, indent=2, ensure_ascii=False)
                print(f"Saved {len(papers)} papers to {filename}")
                
            elif output_format == 'txt':
                with open(filename, 'w', encoding='utf-8') as f:
                    for i, paper in enumerate(papers, 1):
                        f.write(f"=== Paper {i} ===\n")
                        f.write(f"Title: {paper.get('title', 'N/A')}\n")
                        f.write(f"Authors: {', '.join(paper.get('authors', []))}\n")
                        f.write(f"arXiv ID: {paper.get('arxiv_id', 'N/A')}\n")
                        f.write(f"Published: {paper.get('published', 'N/A')}\n")
                        f.write(f"Categories: {', '.join(paper.get('categories', []))}\n")
                        f.write(f"Summary: {paper.get('summary', 'N/A')[:500]}...\n")
                        f.write(f"PDF Link: {next((link['href'] for link in paper.get('links', []) if link.get('rel') == 'related' and 'pdf' in link.get('title', '').lower()), 'N/A')}\n")
                        f.write("\n")
                print(f"Saved {len(papers)} papers to {filename}")
                
            elif output_format == 'csv':
                import csv
                with open(filename, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    # Write header
                    writer.writerow(['Title', 'Authors', 'arXiv ID', 'Published', 'Categories', 'Summary Preview', 'PDF Link'])
                    # Write data
                    for paper in papers:
                        pdf_link = next((link['href'] for link in paper.get('links', []) if link.get('rel') == 'related' and 'pdf' in link.get('title', '').lower()), '')
                        writer.writerow([
                            paper.get('title', ''),
                            '; '.join(paper.get('authors', [])),
                            paper.get('arxiv_id', ''),
                            paper.get('published', ''),
                            '; '.join(paper.get('categories', [])),
                            (paper.get('summary', '')[:200] + '...') if paper.get('summary') else '',
                            pdf_link
                        ])
                print(f"Saved {len(papers)} papers to {filename}")
                
            else:
                print(f"Unsupported output format: {output_format}", file=sys.stderr)
                
        except IOError as e:
            print(f"Error saving to file: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description='Scrape papers from arXiv')
    parser.add_argument('--query', '-q', required=True, help='Search query')
    parser.add_argument('--max-results', '-m', type=int, default=10, help='Maximum number of results (default: 10)')
    parser.add_argument('--start-date', '-s', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', '-e', help='End date (YYYY-MM-DD)')
    parser.add_argument('--category', '-c', help='arXiv category (e.g., cs.AI, cs.LG, quant-ph)')
    parser.add_argument('--output', '-o', choices=['json', 'txt', 'csv'], default='json', help='Output format (default: json)')
    parser.add_argument('--filename', '-f', help='Output filename (optional)')
    parser.add_argument('--delay', '-d', type=float, default=3.0, help='Delay between requests in seconds (default: 3.0)')
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = ArxivScraper(max_results=args.max_results, delay=args.delay)
    
    print(f"Searching arXiv for: {args.query}")
    if args.category:
        print(f"Category: {args.category}")
    if args.start_date:
        print(f"Date range: {args.start_date} to {args.end_date or 'today'}")
    
    # Search for papers
    papers = scraper.search(
        query=args.query,
        start_date=args.start_date,
        end_date=args.end_date,
        category=args.category
    )
    
    if not papers:
        print("No papers found.")
        return
    
    print(f"Found {len(papers)} papers.")
    
    # Display first paper as preview
    if papers:
        print("\n=== First Paper Preview ===")
        first = papers[0]
        print(f"Title: {first.get('title', 'N/A')}")
        print(f"Authors: {', '.join(first.get('authors', []))}")
        print(f"arXiv ID: {first.get('arxiv_id', 'N/A')}")
        print(f"Published: {first.get('published', 'N/A')}")
        print(f"Summary: {first.get('summary', 'N/A')[:300]}...")
    
    # Save to file
    scraper.save_to_file(papers, args.output, args.filename)


if __name__ == "__main__":
    main()


# Example usage:
"""
# Basic search
python arxiv_scraper.py --query "machine learning" --max-results 5

# Search with category
python arxiv_scraper.py --query "transformer" --category cs.CL --max-results 10

# Search with date range
python arxiv_scraper.py --query "quantum" --start-date 2025-01-01 --end-date 2025-03-01

# Save as text file
python arxiv_scraper.py --query "deep learning" --output txt --filename "dl_papers.txt"

# Save as CSV
python arxiv_scraper.py --query "reinforcement learning" --output csv
"""