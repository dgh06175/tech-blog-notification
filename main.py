import requests
import os
from bs4 import BeautifulSoup

BASE_URL_TOSS = "https://toss.tech"
BASE_URL_WOOWAHAN = "https://techblog.woowahan.com/"
BASE_URL_KAKAO = "https://tech.kakao.com"

def fetch_html_from_url(url):
    """URL에서 HTML 내용을 가져옵니다."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def get_latest_post_from_toss():
    """토스 기술 블로그에서 최신 게시글의 링크를 반환합니다."""
    html_content = fetch_html_from_url(BASE_URL_TOSS)
    soup = BeautifulSoup(html_content, 'html.parser')
    ul_toss = soup.find("ul", class_="css-nsslhm e16omkx80")
    latest_post_link_element_toss = ul_toss.find("a") if ul_toss else None
    latest_post_link = latest_post_link_element_toss["href"] if latest_post_link_element_toss else None
    return {
        "title": "N/A",
        "link": f"{BASE_URL_TOSS}{latest_post_link}",
        "date": "N/A"
    }

def get_latest_post_from_woowahan():
    """우아한형제들 기술 블로그에서 최신 게시글의 링크를 반환합니다."""
    html_content = fetch_html_from_url(BASE_URL_WOOWAHAN)
    soup = BeautifulSoup(html_content, 'html.parser')
    posts_div_woowahan = soup.find("div", class_="posts")
    latest_post_link_element_woowahan = posts_div_woowahan.find("div").find("a") if posts_div_woowahan else None
    latest_post_link = latest_post_link_element_woowahan["href"] if latest_post_link_element_woowahan else None
    return {
        "title": "N/A",
        "link": latest_post_link,
        "date": "N/A"
    }


def get_latest_post_from_kakao():
    html_content = fetch_html_from_url(BASE_URL_KAKAO)
    soup = BeautifulSoup(html_content, 'html.parser')
    latest_post_link_element = soup.find("a", {"class": "elementor-post__thumbnail__link"})
    latest_post_link = latest_post_link_element["href"] if latest_post_link_element else None
    return {
        "title": "N/A",
        "link": latest_post_link,
        "date": "N/A"
    }

def save_last_post_link(blog_name, link):
    """최근 스크래핑한 게시글의 링크를 파일에 저장합니다."""
    with open(f"{blog_name}_last_post.txt", "w", encoding="utf-8") as file:
        file.write(link)

def load_last_post_link(blog_name):
    """저장된 게시글의 링크를 로드합니다."""
    file_path = f"{blog_name}_last_post.txt"
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()


def check_new_post_and_notify(blog_name, fetch_function):
    """새로운 게시글이 올라왔는지 확인하고 알림을 보냅니다."""
    # 최신 게시글 정보 가져오기
    latest_post_info = fetch_function()

    # 이전 게시글 링크 로드
    last_post_link = load_last_post_link(blog_name)

    # 새로운 게시글이 올라왔는지 확인
    if not last_post_link or (latest_post_info["link"] != last_post_link):
        # 새로운 게시글의 링크를 출력
        print(latest_post_info['link'])

        # 새로운 게시글 링크 저장
        save_last_post_link(blog_name, latest_post_info["link"])


def delete_last_post_link(blog_name):
    """저장된 게시글의 링크 정보를 삭제합니다."""
    file_path = f"{blog_name}_last_post.txt"
    if os.path.exists(file_path):
        os.remove(file_path)
        return f"'{file_path}' has been deleted."
    else:
        return f"'{file_path}' does not exist."

# 테스트 코드: "Toss" 및 "Woowahan"에 대한 저장된 게시글 정보를 삭제합니다.
# delete_toss_info = delete_last_post_link("Toss")
# delete_woowahan_info = delete_last_post_link("Woowahan")
# delete_kakao_info = delete_last_post_link("Kakao")


if __name__ == "__main__":
    # 각 블로그에서 최신 게시글을 확인합니다.
    check_new_post_and_notify("Toss", get_latest_post_from_toss)
    check_new_post_and_notify("Woowahan", get_latest_post_from_woowahan)
    check_new_post_and_notify("Kakao", get_latest_post_from_kakao)
