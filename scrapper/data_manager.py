import os
import json


class DBManager:
    def __init__(self, blog_name):
        self.blog_name = blog_name
        self.file_path = f"pastData/{blog_name}_link_data.json"

    def save_last_post_link(self, link):
        """게시글 링크를 JSON 파일에 저장"""
        os.makedirs(
            os.path.dirname(self.file_path), exist_ok=True
        )  # 디렉토리 없을경우 생성
        data = {"link": link}
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def link_exists(self, link):
        """주어진 링크가 파일에 저장된 링크와 일치하는지 확인

        :param link: 확인할 링크
        :return: 링크가 파일에 존재하면 True, 그렇지 않으면 False
        """

        # 파일이 존재하지 않거나 파일 크기가 0인 경우
        if not os.path.exists(self.file_path) or os.stat(self.file_path).st_size == 0:
            return False
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data.get("last_post_link") == link
        except (json.JSONDecodeError, OSError):
            return False

    def clear_all_txt_files_in_pastData(self):
        """과거링크 데이터를 모두 삭제"""
        directory = "pastData"
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                os.remove(filepath)
