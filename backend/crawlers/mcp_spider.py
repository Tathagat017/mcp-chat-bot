import scrapy
import json
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import os


class MCPSpider(scrapy.Spider):
    name = 'mcp_spider'
    allowed_domains = ['anthropic.com']
    start_urls = ['https://www.anthropic.com/news/model-context-protocol']
    
    def __init__(self):
        self.visited_urls = set()
        self.extracted_data = []
        self.base_domain = 'https://www.anthropic.com'
        
    def parse(self, response):
        """Parse the main page and extract content"""
        # Extract text content from the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Extract main content
        text_content = self.extract_text_content(soup)
        
        if text_content:
            page_data = {
                'url': response.url,
                'title': self.extract_title(soup),
                'text': text_content,
                'timestamp': self.get_timestamp()
            }
            self.extracted_data.append(page_data)
            
        # Find and follow internal links
        links = response.css('a::attr(href)').getall()
        for link in links:
            absolute_url = urljoin(response.url, link)
            
            # Only follow links within the same domain and related to MCP
            if self.should_follow_link(absolute_url):
                if absolute_url not in self.visited_urls:
                    self.visited_urls.add(absolute_url)
                    yield response.follow(absolute_url, self.parse)
                    
    def extract_text_content(self, soup):
        """Extract clean text content from BeautifulSoup object"""
        # Focus on main content areas
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        
        if not main_content:
            main_content = soup.find('body')
            
        if main_content:
            # Remove navigation, footer, and other non-content elements
            for element in main_content.find_all(['nav', 'footer', 'header', 'aside']):
                element.decompose()
                
            # Extract text and clean it
            text = main_content.get_text(separator=' ', strip=True)
            
            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            
            return text
            
        return ""
    
    def extract_title(self, soup):
        """Extract page title"""
        title = soup.find('title')
        if title:
            return title.get_text().strip()
        
        # Try h1 as fallback
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()
            
        return "Untitled"
    
    def should_follow_link(self, url):
        """Determine if we should follow this link"""
        parsed_url = urlparse(url)
        
        # Must be same domain
        if parsed_url.netloc != 'www.anthropic.com':
            return False
            
        # Skip certain file types
        skip_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.exe']
        if any(url.lower().endswith(ext) for ext in skip_extensions):
            return False
            
        # Skip fragments and query parameters that don't add content
        if '#' in url and '?' not in url:
            return False
            
        # Focus on MCP-related content
        mcp_keywords = ['model-context-protocol', 'mcp', 'context-protocol']
        url_lower = url.lower()
        
        if any(keyword in url_lower for keyword in mcp_keywords):
            return True
            
        # Also include general documentation or blog posts that might reference MCP
        content_keywords = ['docs', 'documentation', 'blog', 'news', 'research']
        if any(keyword in url_lower for keyword in content_keywords):
            return True
            
        return False
    
    def get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def closed(self, reason):
        """Called when spider is closed - save data to JSON file"""
        output_file = os.path.join('data', 'mcp_documentation.json')
        
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.extracted_data, f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"Saved {len(self.extracted_data)} pages to {output_file}")
        print(f"Crawling completed. Saved {len(self.extracted_data)} pages to {output_file}") 