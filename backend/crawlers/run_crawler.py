#!/usr/bin/env python3
"""
Script to run the MCP documentation crawler
"""
import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .mcp_spider import MCPSpider


def run_crawler():
    """Run the MCP spider crawler"""
    
    # Configure Scrapy settings
    settings = {
        'USER_AGENT': 'MCPBot (+https://github.com/your-repo)',
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 16,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'DOWNLOAD_DELAY': 1,  # Be respectful to the server
        'RANDOMIZE_DOWNLOAD_DELAY': 0.5,
        'COOKIES_ENABLED': False,
        'TELNETCONSOLE_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
        },
        'LOG_LEVEL': 'INFO',
    }
    
    # Create and configure the crawler process
    process = CrawlerProcess(settings)
    
    # Add the spider to the process
    process.crawl(MCPSpider)
    
    # Start the crawling process
    print("Starting MCP documentation crawler...")
    process.start()


if __name__ == "__main__":
    run_crawler() 