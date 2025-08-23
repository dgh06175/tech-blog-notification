"""
통합 테스트 스크립트
Firebase Functions 배포 전 로컬 통합 테스트
"""
import sys
import os
from datetime import datetime
import json

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.samsung_scraper import SamsungScraper
from scrapers.kakao_scraper import KakaoScraper
from scrapers.woowahan_scraper import WoowahanScraper
from scrapers.inflab_scraper import InflabScraper
from scrapers.toss_scraper import TossScraper
from scrapers.naver_d2_scraper import NaverD2Scraper
from scrapers.banksalad_scraper import BanksaladScraper


def simulate_scrape_all_blogs():
    """
    main.py의 scrape_all_blogs 함수와 동일한 로직을 시뮬레이션
    """
    print("=== 전체 블로그 스크래핑 시뮬레이션 ===\n")
    
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
    scraping_results = {}
    
    for scraper in scrapers:
        try:
            print(f"스크래핑 중: {scraper.get_blog_name()}...")
            posts = scraper.scrape()
            all_posts.extend(posts)
            scraping_results[scraper.get_blog_name()] = len(posts)
            print(f"✅ {scraper.get_blog_name()}: {len(posts)}개 포스트")
        except Exception as e:
            scraping_results[scraper.get_blog_name()] = f"Error: {str(e)}"
            print(f"❌ {scraper.get_blog_name()}: {str(e)}")
    
    print(f"\n=== 스크래핑 결과 요약 ===")
    print(f"총 포스트 수: {len(all_posts)}개")
    print("블로그별 결과:")
    for blog_name, result in scraping_results.items():
        print(f"  {blog_name}: {result}")
    
    return all_posts, scraping_results


def validate_data_format(posts):
    """
    데이터 포맷 검증
    """
    print(f"\n=== 데이터 포맷 검증 ===")
    
    issues = []
    
    for i, post in enumerate(posts):
        # 필수 필드 확인
        required_fields = ['blog_name', 'title', 'link', 'date']
        for field in required_fields:
            if field not in post:
                issues.append(f"포스트 {i+1}: '{field}' 필드 누락")
        
        # 데이터 타입 확인
        if 'date' in post:
            if post['date'] is not None and not isinstance(post['date'], datetime):
                issues.append(f"포스트 {i+1}: 날짜 타입이 datetime이 아님 ({type(post['date'])})")
        
        # URL 검증
        if 'link' in post:
            if not post['link'].startswith(('http://', 'https://')):
                issues.append(f"포스트 {i+1}: 유효하지 않은 URL 형식")
    
    if issues:
        print("❌ 데이터 포맷 이슈 발견:")
        for issue in issues[:10]:  # 최대 10개만 출력
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... 총 {len(issues)}개 이슈")
    else:
        print("✅ 모든 데이터 포맷이 올바릅니다.")
    
    return len(issues) == 0


def simulate_firestore_upload(posts):
    """
    FireStore 업로드 시뮬레이션 (실제 업로드 없이 로직만 테스트)
    """
    print(f"\n=== FireStore 업로드 시뮬레이션 ===")
    
    try:
        from firestore_uploader import FirestoreUploader
        
        # 업로더 인스턴스 생성 (실제 초기화는 하지 않음)
        uploader = FirestoreUploader.__new__(FirestoreUploader)
        
        results = {"created": 0, "updated": 0, "skipped": 0, "errors": 0}
        
        for post_data in posts:
            try:
                # 포스트 ID 생성 테스트
                post_id = uploader._FirestoreUploader__generate_post_id(post_data)
                
                # FireStore 포맷팅 테스트
                formatted_data = uploader._format_for_firestore(post_data)
                
                # None 값 제거 확인
                if any(v is None for v in formatted_data.values()):
                    results["errors"] += 1
                else:
                    results["created"] += 1
                    
            except Exception as e:
                results["errors"] += 1
                print(f"  ⚠️ 포스트 처리 오류: {str(e)}")
        
        print(f"시뮬레이션 결과:")
        print(f"  생성 예정: {results['created']}개")
        print(f"  오류: {results['errors']}개")
        
        return results
        
    except Exception as e:
        print(f"❌ FireStore 업로드 시뮬레이션 실패: {str(e)}")
        return None


def main():
    """
    전체 통합 테스트 실행
    """
    print("Firebase Functions 배포 전 통합 테스트 시작")
    print("=" * 60)
    
    # 1. 전체 스크래핑 테스트
    all_posts, scraping_results = simulate_scrape_all_blogs()
    
    if not all_posts:
        print("❌ 스크래핑 결과가 없습니다.")
        return
    
    # 2. 데이터 포맷 검증
    format_ok = validate_data_format(all_posts)
    
    # 3. FireStore 업로드 시뮬레이션
    upload_results = simulate_firestore_upload(all_posts)
    
    # 4. 최종 결과
    print(f"\n{'=' * 60}")
    print("=== 통합 테스트 최종 결과 ===")
    print(f"{'=' * 60}")
    
    print(f"📊 스크래핑 결과:")
    print(f"  총 포스트: {len(all_posts)}개")
    success_count = sum(1 for result in scraping_results.values() if isinstance(result, int))
    error_count = len(scraping_results) - success_count
    print(f"  성공한 블로그: {success_count}개")
    print(f"  실패한 블로그: {error_count}개")
    
    print(f"\n📋 데이터 포맷: {'✅ 통과' if format_ok else '❌ 실패'}")
    
    if upload_results:
        print(f"\n💾 FireStore 업로드 준비: ✅ 준비 완료")
        print(f"  처리 가능 포스트: {upload_results['created']}개")
        if upload_results['errors'] > 0:
            print(f"  ⚠️ 오류 예상: {upload_results['errors']}개")
    
    # 샘플 데이터 출력
    print(f"\n📝 샘플 포스트 (처음 3개):")
    for i, post in enumerate(all_posts[:3]):
        print(f"  {i+1}. [{post['blog_name']}] {post['title'][:50]}...")
        print(f"     날짜: {post['date']}")
        print(f"     URL: {post['link']}")
        print()
    
    if format_ok and upload_results and upload_results['errors'] == 0:
        print("🎉 모든 테스트 통과! Firebase Functions 배포 준비가 완료되었습니다.")
    else:
        print("⚠️ 일부 이슈가 있습니다. 위의 결과를 확인해주세요.")


if __name__ == "__main__":
    main()