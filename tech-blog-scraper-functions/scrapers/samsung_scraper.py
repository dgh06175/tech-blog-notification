"""
삼성 기술블로그 RSS 스크래퍼
"""
import feedparser
from typing import List, Dict, Any
from .base_scraper import BaseScraper, Post


class SamsungScraper(BaseScraper):
    def get_blog_name(self) -> str:
        return "Samsung"
    
    def scrape(self) -> List[Dict[str, Any]]:
        rss_url = "https://techblog.samsung.com/rss"
        
        try:
            feed = feedparser.parse(rss_url)
            posts = []
            
            for entry in feed.entries:
                post = Post(
                    blog_name=self.get_blog_name(),
                    title=entry.title,
                    link=entry.link,
                    date=self.parse_date(entry.published if hasattr(entry, 'published') else "")
                )
                posts.append(post.to_dict())
            
            return posts
        except Exception as e:
            print(f"Error scraping Samsung blog: {str(e)}")
            return []