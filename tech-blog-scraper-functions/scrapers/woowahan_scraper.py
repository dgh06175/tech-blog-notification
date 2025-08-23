"""
우아한형제들 기술블로그 RSS 스크래퍼
"""
import ssl
import urllib.request
import feedparser
from typing import List, Dict, Any
from .base_scraper import BaseScraper, Post


class WoowahanScraper(BaseScraper):
    def get_blog_name(self) -> str:
        return "Woowahan"
    
    def scrape(self) -> List[Dict[str, Any]]:
        rss_url = "https://techblog.woowahan.com/feed/"
        
        try:
            # SSL 인증서 검증 비활성화
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            # feedparser에 SSL 컨텍스트를 직접 전달할 수 없으므로
            # urllib로 먼저 데이터를 가져옴
            request = urllib.request.Request(rss_url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            
            with urllib.request.urlopen(request, context=ssl_context) as response:
                rss_data = response.read()
            
            # 문자열로 변환된 RSS 데이터를 feedparser로 파싱
            feed = feedparser.parse(rss_data)
            posts = []
            
            for entry in feed.entries:
                post = Post(
                    blog_name=self.get_blog_name(),
                    title=getattr(entry, 'title', ''),
                    link=getattr(entry, 'link', ''),
                    date=self.parse_date(getattr(entry, 'published', ''))
                )
                posts.append(post.to_dict())
            
            return posts
        except Exception as e:
            print(f"Error scraping Woowahan blog: {str(e)}")
            return []