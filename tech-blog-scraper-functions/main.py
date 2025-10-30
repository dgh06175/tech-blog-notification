"""
Firebase Functions for Tech Blog Scraping
"""

import os
import json
from typing import List, Dict, Any
from firebase_functions import https_fn, scheduler_fn, options
from scrapers.samsung_scraper import SamsungScraper
from scrapers.kakao_scraper import KakaoScraper
from scrapers.woowahan_scraper import WoowahanScraper
from scrapers.inflab_scraper import InflabScraper
from scrapers.toss_scraper import TossScraper
from scrapers.naver_d2_scraper import NaverD2Scraper
from scrapers.banksalad_scraper import BanksaladScraper
from firestore_uploader import FirestoreUploader

# 환경 변수에서 Storage 버킷 이름 로드
STORAGE_BUCKET = os.environ.get("STORAGE_BUCKET")


@https_fn.on_request(timeout_sec=540, memory=options.MemoryOption.GB_1)
def scrape_and_upload_all_blogs(req: https_fn.Request) -> https_fn.Response:
    """모든 기술 블로그를 스크래핑하고 FireStore에 업로드하는 함수"""
    scrapers = [
        SamsungScraper(),
        KakaoScraper(),
        WoowahanScraper(),
        InflabScraper(),
        TossScraper(),
        NaverD2Scraper(),
        BanksaladScraper(),
    ]

    all_posts = []
    scraping_results = {}

    # 스크래핑 로직
    for scraper in scrapers:
        try:
            posts = scraper.scrape()
            all_posts.extend(posts)
            scraping_results[scraper.get_blog_name()] = len(posts)
            print(f"Scraped {len(posts)} posts from {scraper.get_blog_name()}")
        except Exception as e:
            scraping_results[scraper.get_blog_name()] = f"Error: {str(e)}"
            print(f"Error scraping {scraper.__class__.__name__}: {str(e)}")

    # FireStore에 업로드 및 인덱스 갱신
    try:
        uploader = FirestoreUploader(storage_bucket=STORAGE_BUCKET)
        upload_results = uploader.upload_posts(all_posts)

        if upload_results["created"] > 0 or upload_results["updated"] > 0:
            uploader.update_search_index()

        stats = uploader.get_collection_stats()

        return https_fn.Response(
            json.dumps(
                {
                    "scraping_results": scraping_results,
                    "upload_results": upload_results,
                    "collection_stats": stats,
                    "total_scraped": len(all_posts),
                    "message": "Scraping and Index update complete",
                },
                default=str,
            ),
            content_type="application/json",
        )
    except Exception as e:
        return https_fn.Response(
            json.dumps(
                {
                    "scraping_results": scraping_results,
                    "upload_error": str(e),
                    "total_scraped": len(all_posts),
                }
            ),
            status=500,
            content_type="application/json",
        )


@https_fn.on_request()
def scrape_all_blogs(req: https_fn.Request) -> https_fn.Response:
    """모든 기술 블로그를 스크래핑만 하는 함수 (업로드 없음)"""
    scrapers = [
        SamsungScraper(),
        KakaoScraper(),
        WoowahanScraper(),
        InflabScraper(),
        TossScraper(),
        NaverD2Scraper(),
        BanksaladScraper(),
    ]

    all_posts = []

    for scraper in scrapers:
        try:
            posts = scraper.scrape()
            all_posts.extend(posts)
        except Exception as e:
            print(f"Error scraping {scraper.__class__.__name__}: {str(e)}")

    return https_fn.Response(
        json.dumps({"posts": all_posts, "total": len(all_posts)}, default=str),
        content_type="application/json",
    )


@https_fn.on_request(timeout_sec=540, memory=options.MemoryOption.GB_1)
def scrape_single_blog(req: https_fn.Request) -> https_fn.Response:
    """특정 블로그만 스크래핑하는 함수"""
    blog_name = req.args.get("blog")
    upload = req.args.get("upload", "false").lower() == "true"

    if not blog_name:
        return https_fn.Response(
            json.dumps({"error": "blog parameter is required"}),
            status=400,
            content_type="application/json",
        )

    scraper_map = {
        "samsung": SamsungScraper,
        "kakao": KakaoScraper,
        "woowahan": WoowahanScraper,
        "inflab": InflabScraper,
        "toss": TossScraper,
        "naver_d2": NaverD2Scraper,
        "banksalad": BanksaladScraper,
    }

    scraper_class = scraper_map.get(blog_name.lower())
    if not scraper_class:
        return https_fn.Response(
            json.dumps({"error": f"Unknown blog: {blog_name}"}),
            status=400,
            content_type="application/json",
        )

    try:
        scraper = scraper_class()
        posts = scraper.scrape()

        result = {"posts": posts, "total": len(posts)}

        if upload:
            uploader = FirestoreUploader(storage_bucket=STORAGE_BUCKET)
            upload_results = uploader.upload_posts(posts)
            result["upload_results"] = upload_results

            if upload_results["created"] > 0 or upload_results["updated"] > 0:
                uploader.update_search_index()

        return https_fn.Response(
            json.dumps(result, default=str), content_type="application/json"
        )
    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": str(e)}), status=500, content_type="application/json"
        )


@scheduler_fn.on_schedule(
    schedule="0 4 * * *",
    timeout_sec=540,
    memory=options.MemoryOption.GB_1,
)
def scheduled_scrape_and_upload(event: scheduler_fn.ScheduledEvent) -> None:
    """매일 새벽 4시(한국시간)에 자동 실행되는 스크래핑 및 업로드 함수"""
    # [로그] 실행 시작 알림
    print(f"Scheduled scraping started at: {event.schedule_time}")

    # [디버그] 환경 변수 값 확인 (None이 뜨면 안됨)
    print(f"DEBUG_BUCKET: {STORAGE_BUCKET}")

    scrapers = [
        SamsungScraper(),
        KakaoScraper(),
        WoowahanScraper(),
        InflabScraper(),
        TossScraper(),
        NaverD2Scraper(),
        BanksaladScraper(),
    ]

    all_posts = []
    scraping_results = {}

    # 1. 스크래핑 로직 실행
    for scraper in scrapers:
        try:
            posts = scraper.scrape()
            all_posts.extend(posts)
            scraping_results[scraper.get_blog_name()] = len(posts)
            print(f"Scraped {len(posts)} posts from {scraper.get_blog_name()}")
        except Exception as e:
            scraping_results[scraper.get_blog_name()] = f"Error: {str(e)}"
            print(f"Error scraping {scraper.__class__.__name__}: {str(e)}")

    # 2. 업로드 및 인덱스 갱신 로직 (오류 포착 강화)
    try:
        # Uploader 초기화 시 환경 변수 문제 발생 가능성 대비
        uploader = FirestoreUploader(storage_bucket=STORAGE_BUCKET)

        upload_results = uploader.upload_posts(all_posts)

        # [로그] 업로드 성공 여부
        print(f"Upload completed: {upload_results}")
        print(f"Total posts processed: {len(all_posts)}")

        if upload_results["created"] > 0 or upload_results["updated"] > 0:
            print("Updating search index...")
            uploader.update_search_index()

        # 통계 정보 조회
        stats = uploader.get_collection_stats()
        print(f"Collection stats: {stats}")

    except Exception as e:
        # [로그] 치명적인 업로드/인덱싱 오류 발생 시 로그 남기고 함수 종료
        print(f"FATAL_UPLOAD_ERROR: {str(e)}")
        # 이 시점에서 함수 실행이 멈추고 로그가 확실히 남게 됩니다.
        return

    # 모든 로직 성공 시 최종 완료 로그
    print("Scheduled scraping completed successfully.")


@https_fn.on_request()
def get_collection_stats(req: https_fn.Request) -> https_fn.Response:
    """FireStore 컬렉션 통계 조회"""
    try:
        uploader = FirestoreUploader(storage_bucket=STORAGE_BUCKET)
        stats = uploader.get_collection_stats()

        return https_fn.Response(
            json.dumps(stats, default=str), content_type="application/json"
        )
    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": str(e)}), status=500, content_type="application/json"
        )
