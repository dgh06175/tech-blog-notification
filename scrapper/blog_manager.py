from bs4 import BeautifulSoup
import re

BLOGS = {
    "Toss": {
        "KRname": "토스",
        "url": "https://toss.tech",
        "linkParser": lambda soup: [
            "https://toss.tech" + li.find("a")["href"]
            for li in soup.find("ul", class_="css-nsslhm e16omkx80").find_all("li")
        ],
        "titleParser": lambda soup: [
            li.find("a").find("span").text
            for li in soup.find("ul", class_="css-nsslhm e16omkx80").find_all("li")
        ],
        "authorParser": lambda soup: [""],
        "timeParser": lambda soup: [
            li.find("span", text=re.compile(r"\d{4}\. \d{1,2}\. \d{1,2}")).text
            # li.find_all("span")[-1].text
            for li in soup.find("ul", class_="css-nsslhm e16omkx80").find_all("li")
        ],
    },
    "Woowahan": {
        "KRname": "우아한 형제들",
        "url": "https://techblog.woowahan.com",
        "linkParser": lambda soup: [
            (
                div.find("a", {"href": True})["href"]
                if div.find("a", {"href": True})
                else None
            )
            for div in soup.find("div", class_="post-list").find_all(
                "div", class_="post-item"
            )
        ],
        "titleParser": lambda soup: [
            div.find("h2", class_="post-title").text
            for div in soup.find("div", class_="post-list").find_all(
                "div", class_="post-item"
            )
        ],
        "authorParser": lambda soup: [
            div.find("p", class_="post-author")
            .find("span", class_="post-author-name")
            .text
            for div in soup.find("div", class_="post-list").find_all(
                "div", class_="post-item"
            )
        ],
        "timeParser": lambda soup: [
            div.find("p", class_="post-author").find("time").text
            for div in soup.find("div", class_="post-list").find_all(
                "div", class_="post-item"
            )
        ],
    },
    "Kakao": {
        "KRname": "카카오",
        "url": "https://tech.kakao.com/blog",
        "linkParser": lambda soup: [
            article.find("h3", class_="elementor-post__title").find("a")["href"]
            for article in soup.find_all("article")
        ],
        "titleParser": lambda soup: [
            article.find("h3", class_="elementor-post__title").find("a").text
            for article in soup.find_all("article")
        ],
        "authorParser": lambda soup: [
            article.find("div", class_="elementor-post__meta-data")
            .find("span", class_="elementor-post-author")
            .text
            for article in soup.find_all("article")
        ],
        "timeParser": lambda soup: [
            article.find("div", class_="elementor-post__meta-data")
            .find("span", class_="elementor-post-date")
            .text
            for article in soup.find_all("article")
        ],
    },
}


class BlogParser:
    def __init__(self, blog_config):
        self.blog_config = blog_config

    def parse_titles(self, html_content):
        """HTML 내용에서 모든 제목을 파싱한다."""
        soup = BeautifulSoup(html_content, "html.parser")
        return [title.strip() for title in self.blog_config["titleParser"](soup)]

    def parse_links(self, html_content):
        """HTML 내용에서 모든 링크를 파싱한다."""
        soup = BeautifulSoup(html_content, "html.parser")
        return [link for link in self.blog_config["linkParser"](soup)]

    def parse_authors(self, html_content):
        """HTML 내용에서 모든 저자를 파싱한다."""
        soup = BeautifulSoup(html_content, "html.parser")
        return [author.strip() for author in self.blog_config["authorParser"](soup)]

    def parse_times(self, html_content):
        """HTML 내용에서 모든 날짜를 파싱한다."""
        soup = BeautifulSoup(html_content, "html.parser")
        return [time.strip() for time in self.blog_config["timeParser"](soup)]
