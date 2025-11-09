"""
블로그 게시글 태그 자동 분류 스크립트
CSV 파일에서 블로그 데이터를 읽어 OpenAI API를 통해 태그를 생성하고 결과를 저장합니다.
"""

from enum import Enum
from typing import Literal, Optional
from openai import OpenAI
from pydantic import BaseModel, Field
import csv
import os
import sys


# 카테고리 Enum 정의
class BlogCategory(str, Enum):
    FRONTEND = "프론트엔드"
    BACKEND = "백엔드"
    MOBILE = "모바일"
    DEVOPS = "DevOps"
    AI = "AI"
    TEST = "테스트"
    SECURITY = "보안"
    DESIGN = "디자인"
    CONFERENCE = "컨퍼런스"
    PROMOTION = "홍보"
    DATA = "데이터"
    DEV_CULTURE = "개발문화"
    PLANNING = "기획"
    ETC = "기타"


# Pydantic 모델 정의 (Structured Outputs 사용)
class BlogTags(BaseModel):
    """블로그 게시글 태그 분류 결과"""

    link: str = Field(description="블로그 게시글 링크")
    tags: list[BlogCategory] = Field(
        description="선택된 태그 목록 (1~3개)", min_length=1, max_length=3
    )


class BlogTagClassifier:
    """블로그 태그 자동 분류기"""

    SYSTEM_PROMPT = """당신은 블로그 게시글을 분석하여 적절한 카테고리 태그를 선택하는 전문가입니다.

다음 카테고리 중에서 게시글의 내용과 가장 관련이 깊은 태그를 1~3개 선택해주세요:
프론트엔드, 백엔드, 모바일, DevOps, AI, 테스트, 보안
디자인, 컨퍼런스, 홍보, 데이터, 개발문화, 기획, 기타

규칙:
- 반드시 위 카테고리 중에서만 선택, 최소 1개~최대 3개
- 게시글의 핵심 주제와 가장 관련있는 태그를 우선 선택
- 중요: '홍보', '기타', '개발문화' 태그가 선택되는 경우, 해당 태그 하나만 선택해야 합니다 (다른 태그와 함께 선택 불가)
- 나머지 카테고리 중 명확히 해당하는 것이 없을 경우에만 '기타' 선택"""

    def __init__(self, api_key: Optional[str] = None):
        # 환경변수에서 API 키 읽기
        if api_key is None:
            api_key = os.getenv("OPENAI_KEY") or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_KEY 환경변수가 설정되지 않았습니다.")
        self.client = OpenAI(api_key=api_key)

    def classify_blog(
        self, link: str, title: str, content: str = ""
    ) -> Optional[BlogTags]:
        """블로그 게시글의 태그를 분류합니다."""
        user_content = (
            f"제목: {title}\n\n내용: {content}" if content else f"제목: {title}"
        )

        try:
            response = self.client.responses.parse(
                model="gpt-5-mini",
                input=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
                text_format=BlogTags,
            )
            result = response.output_parsed
            if result:
                result.link = link
            return result
        except Exception as e:
            print(f"❌ 오류: {str(e)}")
            return None

    def process_csv(self, input_csv: str, output_csv: str, limit: Optional[int] = None):
        """CSV 파일에서 블로그 데이터를 읽어 태그를 생성하고 저장합니다."""
        if not os.path.exists(input_csv):
            print(f"❌ 파일 없음: {input_csv}")
            return

        with open(input_csv, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        # limit 적용
        if limit:
            rows = rows[:limit]
            print(f"📋 총 {len(rows)}개 처리 시작 (전체 중 일부만 처리)\n")
        else:
            print(f"📋 총 {len(rows)}개 처리 시작\n")

        results = []
        for idx, row in enumerate(rows, 1):
            # 실제 CSV 컬럼명에 맞게 수정
            title = row.get("titles", row.get("title", ""))
            link = row.get("urls", row.get("link", ""))
            content = row.get("contents", row.get("content", ""))

            print(f"[{idx}/{len(rows)}] {title[:40]}...")

            if result := self.classify_blog(link, title, content):
                results.append(
                    {
                        "link": result.link,
                        "title": title,
                        "tags": ", ".join([tag.value for tag in result.tags]),
                    }
                )
                print(f"✅ {', '.join([tag.value for tag in result.tags])}\n")
            else:
                print("⏭️  건너뜀\n")

        if results:
            with open(output_csv, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["link", "title", "tags"])
                writer.writeheader()
                writer.writerows(results)
            print(f"✨ 완료! {len(results)}개 저장 → {output_csv}")
        else:
            print("⚠️  처리된 결과 없음")


def main():
    """메인 함수"""
    # 실제 실행
    classifier = BlogTagClassifier()

    # 처리할 개수 옵션 (예: python script.py 10 → 10개만 처리)
    limit = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None

    if limit:
        print(f"⚡ 처음 {limit}개만 처리합니다.\n")
    else:
        print("⚠️  전체 데이터를 처리합니다. 비용이 많이 발생할 수 있습니다!")
        confirm = input("계속하시겠습니까? (y/N): ")
        if confirm.lower() != "y":
            print("취소되었습니다.")
            return

    classifier.process_csv(
        "data/scrape_results.csv", "blog_tags_result.csv", limit=limit
    )


if __name__ == "__main__":
    main()
