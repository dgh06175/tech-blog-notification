"""
기본 스크래퍼 인터페이스
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import dateutil.parser
import re


@dataclass
class Post:
    """블로그 포스트 데이터 클래스"""
    blog_name: str
    title: str
    link: str
    date: Optional[datetime]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'blog_name': self.blog_name,
            'title': self.title,
            'link': self.link,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S') if self.date else None,
            'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }


class BaseScraper(ABC):
    """기본 스크래퍼 추상 클래스"""
    
    @abstractmethod
    def get_blog_name(self) -> str:
        """블로그 이름 반환"""
        pass
    
    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        """블로그 포스트 스크래핑"""
        pass
    
    def parse_date(self, date_str: str) -> Optional[datetime]:
        """다양한 날짜 형식을 datetime으로 변환 (FireStore 호환)"""
        if not date_str or date_str.strip() == '':
            return None
            
        try:
            # Unix timestamp (milliseconds)
            if date_str.isdigit() and len(date_str) >= 13:
                return datetime.fromtimestamp(int(date_str) / 1000)
            
            # Unix timestamp (seconds)  
            if date_str.isdigit() and len(date_str) == 10:
                return datetime.fromtimestamp(int(date_str))
            
            # ISO 8601 형식 처리
            if 'T' in date_str:
                return dateutil.parser.parse(date_str)
            
            # RFC 2822 형식 (RSS)
            if re.match(r'[A-Za-z]{3},?\s+\d{1,2}\s+[A-Za-z]{3}\s+\d{4}', date_str):
                return dateutil.parser.parse(date_str)
            
            # 기타 일반적인 형식들
            # "2025.07.03", "July 5, 2021", "2021-01-01" 등
            return dateutil.parser.parse(date_str)
            
        except (ValueError, TypeError) as e:
            print(f"날짜 파싱 실패: {date_str} - {str(e)}")
            return None