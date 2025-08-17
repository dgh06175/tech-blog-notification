"""
FireStore 업로드 유틸리티
"""
import json
from typing import List, Dict, Any
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore


class FirestoreUploader:
    def __init__(self, service_account_path: str = None):
        """
        FireStore 업로더 초기화
        
        Args:
            service_account_path: Firebase 서비스 계정 키 파일 경로
        """
        if not firebase_admin._apps:
            if service_account_path:
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred)
            else:
                # Firebase Functions 환경에서는 자동으로 인증됨
                firebase_admin.initialize_app()
        
        self.db = firestore.client()
        
    def upload_posts(self, posts: List[Dict[str, Any]], collection_name: str = "posts") -> Dict[str, int]:
        """
        포스트 데이터를 FireStore에 업로드
        
        Args:
            posts: 업로드할 포스트 리스트
            collection_name: FireStore 컬렉션 이름
            
        Returns:
            업로드 결과 (신규/업데이트 개수)
        """
        results = {"created": 0, "updated": 0, "skipped": 0, "errors": 0}
        
        for post_data in posts:
            try:
                # 포스트 고유 ID 생성 (blog_name + link의 해시)
                post_id = self._generate_post_id(post_data)
                
                # 기존 포스트 확인
                doc_ref = self.db.collection(collection_name).document(post_id)
                existing_post = doc_ref.get()
                
                # FireStore용 데이터 포맷팅
                formatted_data = self._format_for_firestore(post_data)
                
                if existing_post.exists:
                    # 기존 포스트가 있으면 업데이트
                    doc_ref.update({
                        **formatted_data,
                        'updated_at': datetime.now()
                    })
                    results["updated"] += 1
                    print(f"Updated: {post_data.get('title', 'Unknown')}")
                else:
                    # 새 포스트 생성
                    doc_ref.set({
                        **formatted_data,
                        'created_at': datetime.now(),
                        'updated_at': datetime.now()
                    })
                    results["created"] += 1
                    print(f"Created: {post_data.get('title', 'Unknown')}")
                    
            except Exception as e:
                results["errors"] += 1
                print(f"Error uploading post {post_data.get('title', 'Unknown')}: {str(e)}")
        
        return results
    
    def _generate_post_id(self, post_data: Dict[str, Any]) -> str:
        """포스트 고유 ID 생성"""
        import hashlib
        unique_string = f"{post_data['blog_name']}_{post_data['link']}"
        return hashlib.md5(unique_string.encode()).hexdigest()
    
    def _format_for_firestore(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """FireStore용 데이터 포맷팅"""
        # datetime 객체를 FireStore timestamp로 변환
        formatted_data = post_data.copy()
        
        # None 값 제거
        formatted_data = {k: v for k, v in formatted_data.items() if v is not None}
        
        return formatted_data
    
    def get_collection_stats(self, collection_name: str = "posts") -> Dict[str, Any]:
        """컬렉션 통계 조회"""
        try:
            docs = self.db.collection(collection_name).get()
            total_count = len(docs)
            
            # 블로그별 통계
            blog_stats = {}
            for doc in docs:
                data = doc.to_dict()
                blog_name = data.get('blog_name', 'Unknown')
                blog_stats[blog_name] = blog_stats.get(blog_name, 0) + 1
            
            return {
                "total_posts": total_count,
                "blog_stats": blog_stats,
                "last_updated": datetime.now()
            }
        except Exception as e:
            print(f"Error getting collection stats: {str(e)}")
            return {}