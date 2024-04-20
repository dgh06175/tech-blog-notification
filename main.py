import requests
import os
from bs4 import BeautifulSoup


class BlogScraper:
    BLOGS = {
        "Toss": {
            "url": "https://toss.tech",
            "linkParser": lambda soup: "https://toss.tech"
            + soup.find("ul", class_="css-nsslhm e16omkx80").find("a")["href"],
            "titleParser": lambda soup: soup.find("ul", class_="css-nsslhm e16omkx80")
            .find("a")
            .find("span")
            .text,
        },
        "Woowahan": {
            "url": "https://techblog.woowahan.com",
            "linkParser": lambda soup: soup.find("div", class_="post-list")
            .find("div", class_="post-item")
            .find("a")["href"],
            "titleParser": lambda soup: soup.find("div", class_="post-list")
            .find("div", class_="post-item")
            .find("a")
            .find("h2")
            .text,
        },
        "Kakao": {
            "url": "https://tech.kakao.com/blog",
            "linkParser": lambda soup: soup.find(
                "h3", class_="elementor-post__title"
            ).find("a")["href"],
            "titleParser": lambda soup: soup.find("h3", class_="elementor-post__title")
            .find("a")
            .text,
        },
        # "Naver": {
        #     "url": "https://d2.naver.com/",
        #     "linkParser": lambda soup: "https://d2.naver.com" + soup.find("div", class_="cont_post").find("a").text,
        #     "titleParser": lambda soup: soup.find("h2").find("a").text,
        # }
    }

    @staticmethod
    def fetch_html_from_url(url):
        """URL에서 HTML 내용을 가져옵니다."""
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    @classmethod
    def scrape_latest_post(cls, blog_name):
        """특정 블로그에서 최신 게시글의 제목과 링크를 가져옵니다."""
        blog = cls.BLOGS.get(blog_name)
        if not blog:
            return None

        html_content = cls.fetch_html_from_url(blog["url"])
        soup = BeautifulSoup(html_content, "html.parser")

        link = blog["linkParser"](soup)
        if not link:
            return None

        title = blog["titleParser"](soup).strip()

        return {"title": title, "link": link}

    @staticmethod
    def save_last_post_link(blog_name, link):
        """최근 스크래핑한 게시글의 링크를 파일에 저장합니다."""
        with open(f"pastData/{blog_name}_last_post.txt", "w", encoding="utf-8") as file:
            file.write(link)

    @staticmethod
    def load_last_post_link(blog_name):
        """저장된 게시글의 링크를 로드합니다."""
        file_path = f"pastData/{blog_name}_last_post.txt"
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()

    @classmethod
    def check_new_post_and_notify(cls, blog_name):
        """새로운 게시글이 올라왔는지 확인하고 알림을 보냅니다."""
        # 최신 게시글 정보 가져오기
        latest_post_info = cls.scrape_latest_post(blog_name)

        # 이전 게시글 링크 로드
        last_post_link = cls.load_last_post_link(blog_name)

        # 새로운 게시글이 올라왔는지 확인
        if not last_post_link or (latest_post_info["link"] != last_post_link):
            # 새로운 게시글의 링크를 출력
            # print(f"### {blog_name}\n\n[{latest_post_info['title']}]({latest_post_info['link']})\n")
            print(
                f"{blog_name}||{latest_post_info['title']}||{latest_post_info['link']}"
            )
            # 새로운 게시글 링크 저장
            cls.save_last_post_link(blog_name, latest_post_info["link"])


def clear_all_txt_files_in_pastData():
    directory = "pastData"
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "w") as file:
                pass


# 파일 기록 초기화
# clear_all_txt_files_in_pastData()


if __name__ == "__main__":
    # 각 블로그에서 최신 게시글을 확인합니다.
    for blog_name in BlogScraper.BLOGS.keys():
        BlogScraper.check_new_post_and_notify(blog_name)
