"""
네이버 D2 기술블로그 API 스크래퍼
"""
import requests
from typing import List, Dict, Any
from .base_scraper import BaseScraper, Post


class NaverD2Scraper(BaseScraper):
    def get_blog_name(self) -> str:
        return "Naver D2"
    
    def scrape(self) -> List[Dict[str, Any]]:
        api_url = "https://d2.naver.com/api/v1/contents?categoryId=&page=0&size=999"
        
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            posts = []
            if 'content' in data:
                for item in data['content']:
                    post = Post(
                        blog_name=self.get_blog_name(),
                        title=item.get('postTitle', ''),
                        link=f"https://d2.naver.com{item.get('url', '')}",
                        date=self.parse_date(str(item.get('postPublishedAt', '')))
                    )
                    posts.append(post.to_dict())
            
            return posts
        except Exception as e:
            print(f"Error scraping Naver D2 blog: {str(e)}")
            return []