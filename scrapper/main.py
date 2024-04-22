import blog_manager
import data_manager
import html_manager
import json


def main():
    postDatas = []
    blogs = blog_manager.BLOGS
    for blog_name in blogs.keys():
        blog_config = blogs[blog_name]
        postData = getPostData(blogs, blog_name)
        if postData:
            postDatas.append(postData)

    print(json.dumps(postDatas))  # 결과 json 형식으로 출력하여 알림 보내기


def getPostData(blogs, blog_name):
    blog_config = blogs[blog_name]  # 하드코딩된 블로그 정보 딕셔너리 불러오기
    htmlmanager = html_manager.HtmlFetcher  # HTML 클래스 인스턴스 생성
    dbmanager = data_manager.DBManager(blog_name)  # DB 클래스 인스턴스 생성
    parser = blog_manager.BlogParser(blog_config)  # 블로그 파싱 정보 전달하며 파서 인스턴스 생성

    html_content = htmlmanager.fetch_html_from_url(
        blog_config["url"]
    )  # url로 블로그 링크의 html 가져오기

    # dbmanager.clear_all_txt_files_in_pastData()  # DB 삭제

    latest_blog_link = dbmanager.load_last_post_link()  # 로컬에 저장한 최근 링크 정보 가져오기

    blogKRname = blog_config["KRname"]
    title = parser.parse_title(html_content)
    link = parser.parse_link(html_content)

    # 링크 불러오기 실패 or 링크 불러오기 성공, 최근 링크랑 일치 -> None 반환
    if not link or link == latest_blog_link:
        return None

    dbmanager.save_last_post_link(link=link)
    # 링크 불러오기 성곰 - 최근 링크 없음 or 최근 링크랑 불일치 -> 블로그 정보 반환
    return {"blogName": blogKRname, "title": title, "link": link}


if __name__ == "__main__":
    main()
