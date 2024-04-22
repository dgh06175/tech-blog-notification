import os
import json


class DBManager:
    def __init__(self, blog_name):
        self.blog_name = blog_name
        self.file_path = f"pastData/{blog_name}_link_data.json"
        self.links = self.__load_links()

    def add_post_link(self, link):
        """링크를 set에 추가하고 파일에 저장"""
        if link not in self.links:
            self.links.add(link)
            self.__save_links()

    def link_exists(self, link):
        """주어진 링크가 set에 존재하는지 확인"""
        return link in self.links

    def clear_all_files_in_pastData(self):
        """과거링크 데이터를 모두 삭제"""
        directory = "pastData"
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                os.remove(filepath)

    def __load_links(self):
        """파일에서 링크를 로드하고 set으로 반환"""
        if not os.path.exists(self.file_path) or os.stat(self.file_path).st_size == 0:
            return set()
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return set(data.get("links", []))
        except (json.JSONDecodeError, OSError):
            return set()

    def __save_links(self):
        """링크 set을 파일에 저장"""
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump({"links": list(self.links)}, file, ensure_ascii=False, indent=4)
