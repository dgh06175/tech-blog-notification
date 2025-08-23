"""
로컬 테스트용 스크립트
Firebase Functions 없이 스크래퍼들을 개별적으로 테스트
"""
import sys
import os
from typing import Dict, Any

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.samsung_scraper import SamsungScraper
from scrapers.kakao_scraper import KakaoScraper
from scrapers.woowahan_scraper import WoowahanScraper
from scrapers.inflab_scraper import InflabScraper
from scrapers.toss_scraper import TossScraper
from scrapers.naver_d2_scraper import NaverD2Scraper
from scrapers.banksalad_scraper import BanksaladScraper


def test_scraper(scraper_class, scraper_name: str):
    """개별 스크래퍼 테스트"""
    print(f"\n{'='*50}")
    print(f"Testing {scraper_name}")
    print(f"{'='*50}")
    
    try:
        scraper = scraper_class()
        posts = scraper.scrape()
        
        if posts:
            print(f"✅ Success: Found {len(posts)} posts")
            print("\nSample posts:")
            for i, post in enumerate(posts[:3]):  # 처음 3개만 출력
                print(f"{i+1}. {post['title']}")
                print(f"   URL: {post['link']}")
                print(f"   Date: {post['date']}")
                print()
        else:
            print("⚠️  No posts found")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_all_scrapers():
    """모든 스크래퍼 테스트"""
    scrapers = [
        (SamsungScraper, "Samsung Blog"),
        (KakaoScraper, "Kakao Blog"),
        (WoowahanScraper, "Woowahan Blog"),
        (InflabScraper, "Inflab Blog"),
        (TossScraper, "Toss Blog"),
        (NaverD2Scraper, "Naver D2 Blog"),
        (BanksaladScraper, "Banksalad Blog")
    ]
    
    print("Starting scraper tests...")
    
    for scraper_class, scraper_name in scrapers:
        test_scraper(scraper_class, scraper_name)
    
    print(f"\n{'='*50}")
    print("All tests completed!")
    print(f"{'='*50}")


def test_single_scraper(scraper_name: str):
    """특정 스크래퍼만 테스트"""
    scraper_map = {
        'samsung': (SamsungScraper, "Samsung Blog"),
        'kakao': (KakaoScraper, "Kakao Blog"),
        'woowahan': (WoowahanScraper, "Woowahan Blog"),
        'inflab': (InflabScraper, "Inflab Blog"),
        'toss': (TossScraper, "Toss Blog"),
        'naver_d2': (NaverD2Scraper, "Naver D2 Blog"),
        'banksalad': (BanksaladScraper, "Banksalad Blog")
    }
    
    if scraper_name.lower() in scraper_map:
        scraper_class, display_name = scraper_map[scraper_name.lower()]
        test_scraper(scraper_class, display_name)
    else:
        print(f"Unknown scraper: {scraper_name}")
        print(f"Available scrapers: {', '.join(scraper_map.keys())}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 특정 스크래퍼만 테스트
        test_single_scraper(sys.argv[1])
    else:
        # 모든 스크래퍼 테스트
        test_all_scrapers()