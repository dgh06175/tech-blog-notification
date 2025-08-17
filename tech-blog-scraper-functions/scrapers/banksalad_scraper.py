"""
뱅크샐러드 기술블로그 API 스크래퍼 (2단계 API 호출)
"""
import requests
from typing import List, Dict, Any
from .base_scraper import BaseScraper, Post


class BanksaladScraper(BaseScraper):
    def get_blog_name(self) -> str:
        return "Banksalad"
    
    def scrape(self) -> List[Dict[str, Any]]:
        try:
            # 1단계: staticQueryHashes 가져오기
            first_url = "https://blog.banksalad.com/page-data/tech/page-data.json"
            response1 = requests.get(first_url, timeout=10)
            response1.raise_for_status()
            data1 = response1.json()
            
            # staticQueryHashes에서 첫 번째 값 추출
            static_query_hashes = data1.get('staticQueryHashes', [])
            if not static_query_hashes:
                return []
            
            # 2단계: 실제 데이터 가져오기
            second_url = f"https://blog.banksalad.com/page-data/sq/d/{static_query_hashes[0]}.json"
            response2 = requests.get(second_url, timeout=10)
            response2.raise_for_status()
            data2 = response2.json()
            
            posts = []
            # API 응답 구조: data.allMarkdownRemark.edges
            if 'data' in data2 and 'allMarkdownRemark' in data2['data']:
                edges = data2['data']['allMarkdownRemark'].get('edges', [])
                for edge in edges:
                    node = edge.get('node', {})
                    fields = node.get('fields', {})
                    frontmatter = node.get('frontmatter', {})
                    
                    # tech 태그가 있는 포스트만 필터링 (필요시)
                    tags = frontmatter.get('tags', [])
                    
                    post = Post(
                        blog_name=self.get_blog_name(),
                        title=frontmatter.get('title', ''),
                        link=f"https://blog.banksalad.com{fields.get('slug', '')}",
                        date=self.parse_date(frontmatter.get('date', ''))
                    )
                    posts.append(post.to_dict())
            
            return posts
        except Exception as e:
            print(f"Error scraping Banksalad blog: {str(e)}")
            return []