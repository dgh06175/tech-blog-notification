function listBlogNames(posts) {
  const blogNames = posts.map(post => post.blogName);
  return blogNames.join(", ");
}

function formatPostsToMarkdown(posts) {
  return posts.map(post => {
    return `### ${post.blogName}\n\n[${post.title}](${post.link})\n`;
  }).join('\n');
}
  
function getFormattedDate() {
  const currentDate = new Date();
  const kstOffset = 9 * 60 * 60 * 1000; // 한국 시간에 맞게 UTC 기준 시간에 9시간 추가 (밀리초 단위)
  const kstDate = new Date(currentDate.getTime() + kstOffset);
  return `${kstDate.getFullYear()}.${kstDate.getMonth() + 1}.${kstDate.getDate()}`; // 한국 시간에 맞게 포맷
}

function processData(postData) {
  // JSON 형식의 게시글 데이터 파싱
  const posts = JSON.parse(postData);
  console.log("-- posts --");
  console.log(posts);

  // 블로그 이름 문자열 생성
  const blogNames = listBlogNames(posts);
  console.log("-- blogNames --");
  console.log(blogNames);

  // 본문 마크다운 생성
  const markdownPostsBody = formatPostsToMarkdown(posts);
  console.log("-- markdownPostsBody --");
  console.log(markdownPostsBody)
  
  // Date 객체 생성 및 한국 시간 적용
  const formattedDate = getFormattedDate();
  console.log("-- formatteddDate --")
  console.log(formattedDate)

  const issueTitle = `[${formattedDate}] ${blogNames} 블로그 새로운 게시글 업로드`;
  const issueBody = "## 새로운 블로그 게시글 목록\n\n" + markdownPostsBody;
  console.log("-- final Data --")
  console.log(issueTitle)
  console.log(issueBody)

  return { issueTitle, issueBody };
}
 
module.exports = { processData };
  