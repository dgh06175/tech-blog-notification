"""
과거 문서 ID 생성 방식(스킴 포함 raw link 해시) → 현재 방식(_normalize_link 적용 해시)
변경(2025-10-06, f66519c) 이후 마이그레이션 없이 남아있는 중복 게시물 정리 스크립트.

같은 (blog_name, link)를 가진 문서 그룹마다:
- 현재 _generate_post_id 규칙과 ID가 일치하는 문서가 있으면 그 문서만 남기고 나머지는 삭제.
- 일치하는 문서가 없으면(옛 ID만 있고 아직 재스크래핑되지 않은 글. 지금은 중복이 아니어도
  나중에 다시 스크래핑되면 새 ID로 또 하나 생겨 결국 중복이 되므로 미리 옮겨둔다) created_at이
  가장 이른 문서를 골라 새 ID로 마이그레이션(생성 후 기존 문서 삭제)해서 데이터 손실 없이 옮긴다.

기본은 dry-run이며 실제로 쓰기/삭제하려면 --apply 를 명시해야 한다.

사용법:
    python dedupe_posts.py                # dry-run (미리보기만)
    python dedupe_posts.py --apply         # 실제 정리 실행
    python dedupe_posts.py --collection test_tech_blog_posts --apply
"""
import argparse
import sys
import os
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firestore_uploader import FirestoreUploader

BATCH_LIMIT = 400  # Firestore 배치 쓰기 한도(500)보다 여유있게


def load_all_posts(uploader: FirestoreUploader, collection_name: str):
    docs = uploader.db.collection(collection_name).get()
    posts = []
    for doc in docs:
        data = doc.to_dict()
        posts.append({"id": doc.id, "data": data})
    return posts


def group_by_identity(uploader: FirestoreUploader, posts):
    groups = defaultdict(list)
    for post in posts:
        blog_name = post["data"].get("blog_name")
        link = post["data"].get("link")
        if not blog_name or not link:
            continue  # 필수 필드 없는 비정상 문서는 건드리지 않음
        key = (blog_name, uploader._normalize_link(link))
        groups[key].append(post)
    return groups


def plan_actions(uploader: FirestoreUploader, groups):
    """반환: (삭제할 문서 id 목록, 마이그레이션할 (old_id, new_id, data) 목록)"""
    to_delete = []
    to_migrate = []

    for (blog_name, _normalized), members in groups.items():
        expected_id = uploader._generate_post_id(
            {"blog_name": blog_name, "link": members[0]["data"]["link"]}
        )

        canonical = next((m for m in members if m["id"] == expected_id), None)

        if canonical is not None and len(members) == 1:
            continue  # 문서 하나뿐이고 이미 현재 ID 규칙과 일치 -> 손댈 것 없음

        if canonical is None:
            # 새 규칙 ID를 가진 문서가 없음 -> created_at이 가장 이른 문서를 새 ID로 이전.
            # 필드가 없거나 타입이 섞여 있어도(datetime 없는 문서 등) 비교가 깨지지 않도록
            # 항상 float로 변환해서 정렬한다.
            def created_at_key(m):
                val = m["data"].get("created_at") or m["data"].get("scraped_at")
                return val.timestamp() if hasattr(val, "timestamp") else float("inf")

            canonical = min(members, key=created_at_key)
            to_migrate.append((canonical["id"], expected_id, canonical["data"]))

        for m in members:
            if m["id"] != canonical["id"]:
                to_delete.append(m["id"])

    return to_delete, to_migrate


def apply_actions(uploader: FirestoreUploader, collection_name: str, to_delete, to_migrate):
    collection = uploader.db.collection(collection_name)
    ops = []

    for old_id, new_id, data in to_migrate:
        ops.append(("set", new_id, data))
        ops.append(("delete", old_id, None))

    for doc_id in to_delete:
        ops.append(("delete", doc_id, None))

    for i in range(0, len(ops), BATCH_LIMIT):
        batch = uploader.db.batch()
        for kind, doc_id, data in ops[i : i + BATCH_LIMIT]:
            ref = collection.document(doc_id)
            if kind == "set":
                batch.set(ref, data)
            else:
                batch.delete(ref)
        batch.commit()
        print(f"  배치 커밋: {i + len(ops[i:i + BATCH_LIMIT])}/{len(ops)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", default="posts", help="대상 컬렉션 이름 (기본: posts)")
    parser.add_argument("--apply", action="store_true", help="실제로 삭제/마이그레이션 실행 (기본은 dry-run)")
    args = parser.parse_args()

    service_account_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    uploader = FirestoreUploader(service_account_path) if service_account_path else FirestoreUploader()

    print(f"=== '{args.collection}' 컬렉션 중복 문서 조사 ({'dry-run' if not args.apply else 'APPLY'}) ===\n")

    posts = load_all_posts(uploader, args.collection)
    print(f"전체 문서: {len(posts)}개")

    groups = group_by_identity(uploader, posts)
    dup_groups = {k: v for k, v in groups.items() if len(v) > 1}
    print(f"중복 그룹(같은 blog_name+link): {len(dup_groups)}개\n")

    to_delete, to_migrate = plan_actions(uploader, groups)

    print(f"삭제 예정(순수 중복, 이미 새 ID 문서가 있음): {len(to_delete)}개")
    print(f"마이그레이션 예정(새 ID 문서가 없어 옮겨야 함): {len(to_migrate)}개\n")

    if to_migrate:
        print("마이그레이션 예시 (최대 5개):")
        for old_id, new_id, data in to_migrate[:5]:
            print(f"  {old_id} -> {new_id}  ({data.get('blog_name')}: {data.get('title', '')[:40]})")
        print()

    if not args.apply:
        print("dry-run 모드입니다. 실제로 반영하려면 --apply 를 붙여서 다시 실행하세요.")
        return

    print("실제 정리를 시작합니다...")
    apply_actions(uploader, args.collection, to_delete, to_migrate)
    print("\n완료.")


if __name__ == "__main__":
    main()
