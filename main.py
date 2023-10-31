import os
import requests
from bs4 import BeautifulSoup

BASE_URLS = {
    "Toss": "https://toss.tech",
    "Woowahan": "https://techblog.woowahan.com/",
    "Kakao": "https://tech.kakao.com/blog"
}

FETCH_FUNCTIONS = {
    "Toss": lambda soup: soup.find("ul", class_="css-nsslhm e16omkx80"),
    "Woowahan": lambda soup: soup.find("div", class_="posts"),
    "Kakao": lambda soup: soup.find("div", {"class": "elementor-post__text"})
}


def fetch_html(url):
    """Fetch HTML content from a given URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def get_latest_post(blog_name, soup):
    """Extract latest post information based on the blog name."""
    element = FETCH_FUNCTIONS[blog_name](soup)
    post_link_element = element.find("a") if element else None
    post_link = post_link_element["href"] if post_link_element else None
    post_title = post_link_element.text.strip() if post_link_element else "N/A"

    return post_title, post_link


def read_last_post(blog_name):
    """Read the last post link from the file."""
    file_path = f"pastData/{blog_name}_last_post.txt"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    return None


def write_last_post(blog_name, link):
    """Write the latest post link to the file."""
    with open(f"pastData/{blog_name}_last_post.txt", "w", encoding="utf-8") as file:
        file.write(link)


def check_and_notify_new_post(blog_name):
    """Check for a new post and print the details if found."""
    soup = BeautifulSoup(fetch_html(BASE_URLS[blog_name]), 'html.parser')
    title, link = get_latest_post(blog_name, soup)

    if link != read_last_post(blog_name):
        print(f"### {blog_name}\n\n[{title}]({link})\n")
        write_last_post(blog_name, link)


if __name__ == "__main__":
    for blog in BASE_URLS.keys():
        check_and_notify_new_post(blog)
