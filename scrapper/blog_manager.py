from bs4 import BeautifulSoup

BLOGS = {
    "Toss": {
        "KRname": "토스",
        "url": "https://toss.tech",
        "linkParser": lambda soup: "https://toss.tech"
        + soup.find("ul", class_="css-nsslhm e16omkx80").find("a")["href"],
        "titleParser": lambda soup: soup.find("ul", class_="css-nsslhm e16omkx80")
        .find("a")
        .find("span")
        .text,
    },
    "Woowahan": {
        "KRname": "우아한 형제들",
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
        "KRname": "카카오",
        "url": "https://tech.kakao.com/blog",
        "linkParser": lambda soup: soup.find("h3", class_="elementor-post__title").find(
            "a"
        )["href"],
        "titleParser": lambda soup: soup.find("h3", class_="elementor-post__title")
        .find("a")
        .text,
    },
    # "Naver": {
    #     "url": "https://d2.naver.com/",
    #     "linkParser": lambda soup: "https://d2.naver.com"
    #     + soup.find("div", class_="cont_post").find("a")["href"],
    #     "titleParser": lambda soup: soup.find("div", class_="cont_post")
    #     .find("a")
    #     .text,
    # },
}


class BlogParser:
    def __init__(self, blog_config):
        self.blog_config = blog_config

    def parse_title(self, html_content):
        """HTML 내용에서 제목을 파싱한다."""
        soup = BeautifulSoup(html_content, "html.parser")
        return self.blog_config["titleParser"](soup).strip()

    def parse_link(self, html_content):
        """HTML 내용에서 링크를 파싱한다."""
        soup = BeautifulSoup(html_content, "html.parser")
        return self.blog_config["linkParser"](soup).strip()
