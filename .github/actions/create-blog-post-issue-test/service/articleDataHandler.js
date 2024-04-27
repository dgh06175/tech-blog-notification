const fs = require('fs');
const path = require('path');

const blogs = [
  { name: "토스", file: "Toss" },
  { name: "우아한 형제들", file: "Woowahan" },
  { name: "카카오", file: "Kakao" }
];

function readJsonFile(filename) {
  return new Promise((resolve, reject) => {
    fs.readFile(
      path.join(
        __dirname, "..", "..", "..", "..", "database", "new", `${filename}_new.json`
      ),
      'utf8',
      (err, data) => {
        if (err) reject(err);
        else resolve(JSON.parse(data));
      });
  });
}

function generateMarkdownForBlog(name, posts) {
  if (!posts || posts.length === 0) {
    return ""
  }
  let markdown = `## ${name}\n\n`;
  posts.forEach(post => {
    markdown += `### [${post.title}](${post.link})\n`;
    markdown += `> ${post.author || "저자 없음"}\n`;
    markdown += `> ${post.date}\n\n`;
  });
  return markdown;
}

async function formatBlogMarkdown() {
  let issueBody = "# 새로운 블로그 게시글 목록\n\n";
  let newBlogNames = []
  const date = new Date().toISOString().split('T')[0].replace(/-/g, '. ');
  try {
    const blogDataPromises = blogs.map(blog => readJsonFile(blog.file));
    const blogDataResults = await Promise.all(blogDataPromises);
    blogDataResults.forEach((data, index) => {
      const markdown = generateMarkdownForBlog(blogs[index].name, data);
      if (markdown) {
        issueBody += markdown
        newBlogNames.push(blogs[index].name)
      }
    });

    const issueTitle = `[${date}] ${newBlogNames.join(', ')} 블로그 새로운 게시글 업로드`;
    return { issueTitle, issueBody };
  } catch (error) {
    console.error('issueBody markdown 생성 에러:', error);
  }
}

module.exports = { formatBlogMarkdown }