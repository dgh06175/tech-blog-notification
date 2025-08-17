"""
FireStore 업로드 기능 테스트
"""
import sys
import os
from datetime import datetime

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.samsung_scraper import SamsungScraper
from scrapers.kakao_scraper import KakaoScraper
from firestore_uploader import FirestoreUploader


def test_firestore_upload():
    """FireStore 업로드 테스트 (로컬 환경에서는 서비스 계정 키 필요)"""
    print("=== FireStore 업로드 테스트 ===\n")
    
    # 테스트용으로 Samsung 블로그에서 몇 개 포스트만 가져오기
    try:
        print("1. Samsung 블로그 스크래핑...")
        samsung_scraper = SamsungScraper()
        samsung_posts = samsung_scraper.scrape()
        print(f"   Samsung: {len(samsung_posts)} posts")
        
        print("2. Kakao 블로그 스크래핑...")
        kakao_scraper = KakaoScraper()
        kakao_posts = kakao_scraper.scrape()
        print(f"   Kakao: {len(kakao_posts)} posts")
        
        # 테스트용으로 처음 3개 포스트만 사용
        test_posts = samsung_posts[:2] + kakao_posts[:2]
        print(f"\n3. 테스트용 포스트 선택: {len(test_posts)}개")
        
        for i, post in enumerate(test_posts):
            print(f"   {i+1}. {post['title'][:50]}...")
            print(f"      Date: {post['date']} (Type: {type(post['date'])})")
        
        print("\n4. FireStore 업로드 시도...")
        
        # 환경 변수에서 서비스 계정 키 경로 확인
        service_account_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if service_account_path:
            print(f"   서비스 계정 키 파일: {service_account_path}")
            uploader = FirestoreUploader(service_account_path)
        else:
            print("   서비스 계정 키가 설정되지 않음. Firebase Functions 환경 사용 시도...")
            uploader = FirestoreUploader()
        
        # 업로드 실행
        upload_results = uploader.upload_posts(test_posts, "test_tech_blog_posts")
        
        print("\n5. 업로드 결과:")
        print(f"   생성: {upload_results['created']}개")
        print(f"   업데이트: {upload_results['updated']}개")
        print(f"   건너뜀: {upload_results['skipped']}개")
        print(f"   오류: {upload_results['errors']}개")
        
        # 통계 조회
        print("\n6. 컬렉션 통계:")
        stats = uploader.get_collection_stats("test_tech_blog_posts")
        if stats:
            print(f"   총 포스트: {stats.get('total_posts', 0)}개")
            print(f"   블로그별 통계: {stats.get('blog_stats', {})}")
        
        print("\n✅ FireStore 업로드 테스트 완료!")
        
    except Exception as e:
        print(f"\n❌ FireStore 업로드 테스트 실패: {str(e)}")
        print("\n참고:")
        print("- 로컬 테스트를 위해서는 Firebase 서비스 계정 키가 필요합니다.")
        print("- GOOGLE_APPLICATION_CREDENTIALS 환경 변수를 설정하거나")
        print("- Firebase Functions 환경에서 테스트하세요.")


def test_data_format():
    """데이터 포맷 검증 테스트"""
    print("\n=== 데이터 포맷 검증 테스트 ===\n")
    
    try:
        # Samsung 블로그에서 1개 포스트만 가져와서 포맷 확인
        scraper = SamsungScraper()
        posts = scraper.scrape()
        
        if posts:
            sample_post = posts[0]
            print("샘플 포스트 데이터:")
            print(f"  블로그: {sample_post['blog_name']}")
            print(f"  제목: {sample_post['title']}")
            print(f"  링크: {sample_post['link']}")
            print(f"  날짜: {sample_post['date']} (타입: {type(sample_post['date'])})")
            
            # FireStore 포맷팅 테스트
            uploader = FirestoreUploader()
            formatted_data = uploader._format_for_firestore(sample_post)
            
            print("\nFireStore 포맷팅 결과:")
            for key, value in formatted_data.items():
                print(f"  {key}: {value} (타입: {type(value)})")
            
            print("\n✅ 데이터 포맷 검증 완료!")
        
    except Exception as e:
        print(f"❌ 데이터 포맷 검증 실패: {str(e)}")


if __name__ == "__main__":
    # 데이터 포맷 먼저 검증
    test_data_format()
    
    # FireStore 업로드 테스트
    test_firestore_upload()