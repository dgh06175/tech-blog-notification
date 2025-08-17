"""
인프랩 기술블로그 API 스크래퍼
"""
import requests
from typing import List, Dict, Any
from .base_scraper import BaseScraper, Post


class InflabScraper(BaseScraper):
    def get_blog_name(self) -> str:
        return "Inflab"
    
    def scrape(self) -> List[Dict[str, Any]]:
        api_url = "https://tech.inflab.com/page-data/index/page-data.json"
        
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            posts = []
            # API 응답 구조: result.data.allMarkdownRemark.edges
            if 'result' in data and 'data' in data['result']:
                result_data = data['result']['data']
                if 'allMarkdownRemark' in result_data and 'edges' in result_data['allMarkdownRemark']:
                    for edge in result_data['allMarkdownRemark']['edges']:
                        node = edge.get('node', {})
                        frontmatter = node.get('frontmatter', {})
                        fields = node.get('fields', {})
                        
                        post = Post(
                            blog_name=self.get_blog_name(),
                            title=frontmatter.get('title', ''),
                            link=f"https://tech.inflab.com{fields.get('slug', '')}",
                            date=self.parse_date(frontmatter.get('date', ''))
                        )
                        posts.append(post.to_dict())
            
            return posts
        except Exception as e:
            print(f"Error scraping Inflab blog: {str(e)}")
            return []