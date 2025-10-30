"""
FireStore 업로드 유틸리티
"""

import json
from typing import List, Dict, Any
from datetime import datetime, timezone
from urllib.parse import urlparse
from dateutil import parser as date_parser
import firebase_admin
from firebase_admin import credentials, firestore, storage


class FirestoreUploader:
    def __init__(self, service_account_path: str = None, storage_bucket: str = None):
        """
        FireStore 업로더 초기화

        Args:
            service_account_path: Firebase 서비스 계정 키 파일 경로
            storage_bucket: Firebase Storage 버킷 이름
        """
        if not firebase_admin._apps:
            options = {}
            if storage_bucket:
                options["storageBucket"] = storage_bucket

            if service_account_path:
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred, options)
            else:
                # 환경 변수나 Cloud Functions 환경 사용 시
                firebase_admin.initialize_app(options=options if options else None)

        self.db = firestore.client()

        # Storage 버킷 인스턴스 초기화
        try:
            self.bucket = storage.bucket()
        except Exception:
            self.bucket = None
            print(
                "Warning: Storage bucket not initialized. Search index upload will fail."
            )

    def upload_posts(
        self, posts: List[Dict[str, Any]], collection_name: str = "posts"
    ) -> Dict[str, int]:
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
                formatted_data = self._format_for_firestore(
                    post_data, include_scraped_at=not existing_post.exists
                )

                if existing_post.exists:
                    existing_data = existing_post.to_dict()
                    changes = self._detect_changes(existing_data, formatted_data)

                    if not changes:
                        results["skipped"] += 1
                        continue

                    changes["updated_at"] = datetime.now(timezone.utc)
                    doc_ref.update(changes)
                    results["updated"] += 1
                    print(f"Updated: {post_data.get('title', 'Unknown')}")
                else:
                    # 새 포스트 생성
                    now_ts = datetime.now(timezone.utc)
                    doc_ref.set(
                        {
                            **formatted_data,
                            "created_at": formatted_data.get("created_at", now_ts),
                            "updated_at": formatted_data.get("updated_at", now_ts),
                            "scraped_at": formatted_data.get("scraped_at", now_ts),
                        }
                    )
                    results["created"] += 1
                    print(f"Created: {post_data.get('title', 'Unknown')}")

            except Exception as e:
                results["errors"] += 1
                print(
                    f"Error uploading post {post_data.get('title', 'Unknown')}: {str(e)}"
                )

        return results

    def update_search_index(
        self, collection_name: str = "posts", file_path: str = "search/titles.json"
    ):
        """
        Firestore의 모든 포스트 제목을 추출하여 Storage에 JSON으로 저장

        Args:
            collection_name: 대상 컬렉션
            file_path: Storage에 저장될 파일 경로
        """
        if not self.bucket:
            print("Error: Storage bucket is not configured.")
            return

        print("검색 인덱스(Title JSON) 생성 시작...")

        try:
            # 1. 효율적인 읽기
            docs = self.db.collection(collection_name).select(["title"]).stream()

            titles = []
            for doc in docs:
                data = doc.to_dict()
                if "title" in data and data["title"]:
                    titles.append(data["title"])

            # 2. JSON 직렬화
            json_data = json.dumps(titles, ensure_ascii=False)

            # 3. Storage 업로드
            blob = self.bucket.blob(file_path)

            # 메타데이터 설정
            blob.cache_control = "public, max-age=3600"  # 1시간 캐싱

            blob.upload_from_string(json_data, content_type="application/json")

            print(f"성공: {len(titles)}개의 제목이 {file_path}에 저장되었습니다.")

        except Exception as e:
            print(f"검색 인덱스 생성 중 오류 발생: {str(e)}")

    def _generate_post_id(self, post_data: Dict[str, Any]) -> str:
        """포스트 고유 ID 생성"""
        import hashlib

        normalized_link = self._normalize_link(post_data["link"])
        unique_string = f"{post_data['blog_name']}_{normalized_link}"
        return hashlib.md5(unique_string.encode()).hexdigest()

    def _normalize_link(self, link: str) -> str:
        """링크에서 프로토콜을 제거해 중복 검사 내에서 http/https를 동일하게 취급."""
        parsed = urlparse(link)
        # netloc은 대소문자 구분이 없으므로 소문자로 맞춰 중복 가능성을 줄인다.
        netloc = parsed.netloc.lower()
        path = parsed.path or ""
        query = f"?{parsed.query}" if parsed.query else ""
        fragment = f"#{parsed.fragment}" if parsed.fragment else ""
        return f"{netloc}{path}{query}{fragment}"

    def _to_timestamp(self, value: Any) -> Any:
        """FireStore에서 timestamp로 저장될 값을 datetime으로 강제 변환."""
        if value is None:
            return None

        if isinstance(value, datetime):
            return value

        if isinstance(value, (int, float)):
            try:
                # 밀리초 단위로 들어오는 값을 고려
                if value > 1e12:
                    return datetime.fromtimestamp(value / 1000, tz=timezone.utc)
                return datetime.fromtimestamp(value, tz=timezone.utc)
            except Exception:
                return None

        if isinstance(value, str) and value.strip():
            try:
                parsed = date_parser.parse(value)
                return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
            except Exception:
                return None

        return None
        return None

    def _fields_equal(self, a: Any, b: Any) -> bool:
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a.replace(microsecond=0) == b.replace(microsecond=0)
        return a == b

    def _detect_changes(
        self, existing: Dict[str, Any], new_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """기존 문서와 비교해 변경된 필드만 반환."""
        changes = {}
        for key, value in new_data.items():
            if key in ("created_at", "scraped_at"):
                continue
            if not self._fields_equal(existing.get(key), value):
                changes[key] = value
        return changes

    def _format_for_firestore(
        self, post_data: Dict[str, Any], include_scraped_at: bool = True
    ) -> Dict[str, Any]:
        """FireStore용 데이터 포맷팅"""
        allowed_fields = {
            "blog_name",
            "title",
            "link",
            "date",
            "scraped_at",
            "created_at",
            "updated_at",
        }
        filtered_data = {k: v for k, v in post_data.items() if k in allowed_fields}

        formatted_data: Dict[str, Any] = {}

        # 필수 문자열 필드
        for key in ("blog_name", "title", "link"):
            value = filtered_data.get(key)
            if value is None:
                raise ValueError(f"Missing required field: {key}")
            formatted_data[key] = str(value)

        # 타임스탬프 필드
        date_value = self._to_timestamp(filtered_data.get("date"))
        if date_value:
            formatted_data["date"] = date_value

        if include_scraped_at:
            scraped_at_value = self._to_timestamp(filtered_data.get("scraped_at"))
            formatted_data["scraped_at"] = (
                scraped_at_value or datetime.now(timezone.utc)
            )

        created_at_value = self._to_timestamp(filtered_data.get("created_at"))
        if created_at_value:
            formatted_data["created_at"] = created_at_value

        updated_at_value = self._to_timestamp(filtered_data.get("updated_at"))
        if updated_at_value:
            formatted_data["updated_at"] = updated_at_value

        return formatted_data

    def get_collection_stats(self, collection_name: str = "posts") -> Dict[str, Any]:
        """컬렉션 통계 조회 (최적화 버전)"""
        try:
            # [최적화] 모든 필드를 가져오지 않고 'blog_name'만 가져옵니다.
            docs = self.db.collection(collection_name).select(["blog_name"]).stream()

            total_count = 0
            blog_stats = {}

            for doc in docs:
                total_count += 1
                data = doc.to_dict()
                # 필드가 없을 경우를 대비해 get 사용
                blog_name = data.get("blog_name", "Unknown")
                blog_stats[blog_name] = blog_stats.get(blog_name, 0) + 1

            return {
                "total_posts": total_count,
                "blog_stats": blog_stats,
                "last_updated": datetime.now(timezone.utc),
            }
        except Exception as e:
            print(f"Error getting collection stats: {str(e)}")
            return {}
