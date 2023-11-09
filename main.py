import requests
import os
from bs4 import BeautifulSoup


class BlogScraper:
    BLOGS = {
        "Toss": {
            "url": "https://toss.tech",
            "linkParser": lambda soup: "https://toss.tech/" + soup.find("ul", class_="css-nsslhm e16omkx80").find("a")["href"],
            "titleParser": lambda soup: soup.find("ul", class_="css-nsslhm e16omkx80").find("a").find("span").text
        },
        "Woowahan": {
            "url": "https://techblog.woowahan.com",
            "linkParser": lambda soup: soup.find("div", class_="posts").find("div").find("a")["href"],
            "titleParser": lambda soup: soup.find("div", class_="posts").find("div").find("a").find("h2").text
        },
        "Kakao": {
            "url": "https://tech.kakao.com/blog",
            "linkParser": lambda soup: soup.find("div", {"class": "list_post"}).find("a")["href"],
            "titleParser": lambda soup: soup.find("div", {"class": "list_post"}).find("a").find("strong").text.strip()
        }
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
        soup = BeautifulSoup(html_content, 'html.parser')

        link = blog["linkParser"](soup)
        if not link:
            return None

        title = blog["titleParser"](soup).strip()

        return {
            "title": title,
            "link": link
        }

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
수
# clear_all_txt_files_in_pastData()


if __name__ == "__main__":
    # 각 블로그에서 최신 게시글을 확인합니다.
    for blog_name in BlogScraper.BLOGS.keys():
        BlogScraper.check_new_post_and_notify(blog_name)
