"""
Firebase Functions for Tech Blog Scraping
"""
import json
from typing import List, Dict, Any
from firebase_functions import https_fn
from scrapers.samsung_scraper import SamsungScraper
from scrapers.kakao_scraper import KakaoScraper
from scrapers.woowahan_scraper import WoowahanScraper
from scrapers.inflab_scraper import InflabScraper
from scrapers.toss_scraper import TossScraper
from scrapers.naver_d2_scraper import NaverD2Scraper
from scrapers.banksalad_scraper import BanksaladScraper


@https_fn.on_request()
def scrape_all_blogs(req: https_fn.Request) -> https_fn.Response:
    """
    모든 기술 블로그를 스크래핑하는 함수
    """
    scrapers = [
        SamsungScraper(),
        KakaoScraper(),
        WoowahanScraper(),
        InflabScraper(),
        TossScraper(),
        NaverD2Scraper(),
        BanksaladScraper()
    ]
    
    all_posts = []
    
    for scraper in scrapers:
        try:
            posts = scraper.scrape()
            all_posts.extend(posts)
        except Exception as e:
            print(f"Error scraping {scraper.__class__.__name__}: {str(e)}")
    
    return https_fn.Response(
        json.dumps({"posts": all_posts, "total": len(all_posts)}),
        content_type="application/json"
    )


@https_fn.on_request()
def scrape_single_blog(req: https_fn.Request) -> https_fn.Response:
    """
    특정 블로그만 스크래핑하는 함수
    """
    blog_name = req.args.get('blog')
    
    if not blog_name:
        return https_fn.Response(
            json.dumps({"error": "blog parameter is required"}),
            status=400,
            content_type="application/json"
        )
    
    scraper_map = {
        'samsung': SamsungScraper,
        'kakao': KakaoScraper,
        'woowahan': WoowahanScraper,
        'inflab': InflabScraper,
        'toss': TossScraper,
        'naver_d2': NaverD2Scraper,
        'banksalad': BanksaladScraper
    }
    
    scraper_class = scraper_map.get(blog_name.lower())
    if not scraper_class:
        return https_fn.Response(
            json.dumps({"error": f"Unknown blog: {blog_name}"}),
            status=400,
            content_type="application/json"
        )
    
    try:
        scraper = scraper_class()
        posts = scraper.scrape()
        return https_fn.Response(
            json.dumps({"posts": posts, "total": len(posts)}),
            content_type="application/json"
        )
    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=500,
            content_type="application/json"
        )