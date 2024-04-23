import requests


class HtmlFetcher:
    def fetch_html_from_url(self, url):
        """URL에서 HTML 내용을 가져온다.

        :param url: HTML을 가져올 웹 페이지의 URL
        :return: 웹 페이지의 HTML 내용을 문자열로 반환
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise ConnectionError(
                f"[ERROR] url에서 HTML 응답을 가져오는데 실패했습니다: {e}"
            )
