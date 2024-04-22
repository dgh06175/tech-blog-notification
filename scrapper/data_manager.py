import os


class DBManager:
    def __init__(self, blog_name):
        self.blog_name = blog_name
        self.file_path = f"pastData/{blog_name}_last_post.txt"

    def save_last_post_link(self, link):
        """게시글 링크를 파일에 저장"""
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(link)

    def load_last_post_link(self):
        """파일에서 게시글 링크를 로드"""
        if not os.path.exists(self.file_path):
            return None
        with open(self.file_path, "r", encoding="utf-8") as file:
            return file.read().strip()

    def clear_all_txt_files_in_pastData(self):
        """과거링크 데이터를 모두 삭제"""
        directory = "pastData"
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                filepath = os.path.join(directory, filename)
                with open(filepath, "w") as file:
                    pass
