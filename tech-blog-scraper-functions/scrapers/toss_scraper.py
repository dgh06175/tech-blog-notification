"""
토스 기술블로그 API 스크래퍼
"""
import requests
from typing import List, Dict, Any
from .base_scraper import BaseScraper, Post


class TossScraper(BaseScraper):
    def get_blog_name(self) -> str:
        return "Toss"
    
    def scrape(self) -> List[Dict[str, Any]]:
        api_url = "https://api-public.toss.im/api-public/v3/ipd-thor/api/v1/workspaces/15/posts?size=999&categoriesSlug=tech"
        
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            posts = []
            if 'success' in data and 'results' in data['success']:
                for item in data['success']['results']:
                    post = Post(
                        blog_name=self.get_blog_name(),
                        title=item.get('title', ''),
                        link=f"https://toss.tech/article/{item.get('key', '')}",
                        date=self.parse_date(item.get('publishedTime', ''))
                    )
                    posts.append(post.to_dict())
            
            return posts
        except Exception as e:
            print(f"Error scraping Toss blog: {str(e)}")
            return []