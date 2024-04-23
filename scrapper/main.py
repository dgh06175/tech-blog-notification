import blog_manager
import data_manager
import html_manager
import json


def main():
    post_datas = collect_blog_posts()
    if post_datas:
        print(json.dumps(post_datas))  # 결과 json 형식으로 출력하여 알림 보내기


def collect_blog_posts():
    post_datas = []
    blogs = blog_manager.BLOGS
    for blog_name, blog_config in blogs.items():
        post_data = get_post_data(blog_config, blog_name)
        if post_data:
            post_datas.append(post_data)
    return post_datas


def get_post_data(blog_config, blog_name):
    html_fetcher = html_manager.HtmlFetcher()  # HTML 클래스 인스턴스 생성
    db_manager = data_manager.DBManager(blog_name)  # DB 클래스 인스턴스 생성
    blog_parser = blog_manager.BlogParser(blog_config)  # 파서 인스턴스 생성

    # url로 블로그 링크의 html 가져오기
    html_content = html_fetcher.fetch_html_from_url(blog_config["url"])
    if not html_content:
        return None
    # db_manager.clear_all_files_in_pastData()  # DB 삭제

    title = blog_parser.parse_title(html_content)
    link = blog_parser.parse_link(html_content)

    # 링크 불러오기 성곰 - DB에 존재하지 않는 링크 -> 블로그 정보 반환
    if link and not db_manager.link_exists(link):
        db_manager.add_post_link(link)
        return {"blogName": blog_config["KRname"], "title": title, "link": link}

    # 링크 불러오기 실패 or 링크 불러오기 성공했고, DB에 이미 존재하는 링크일때 -> None 반환
    return None


def test():
    blogs = blog_manager.BLOGS
    for blog_name, blog_config in blogs.items():
        html_fetcher = html_manager.HtmlFetcher()  # HTML 클래스 인스턴스 생성
        db_manager = data_manager.DBManager(blog_name)  # DB 클래스 인스턴스 생성
        blog_parser = blog_manager.BlogParser(blog_config)  # 파서 인스턴스 생성

        html_content = html_fetcher.fetch_html_from_url(blog_config["url"])
        if not html_content:
            return None

        title = blog_parser.parse_titles(html_content)
        link = blog_parser.parse_links(html_content)
        print("\n\n###" + blog_name + "###")
        print("title: ", title)
        print()
        print("link: ", link)


if __name__ == "__main__":
    # main()
    test()
