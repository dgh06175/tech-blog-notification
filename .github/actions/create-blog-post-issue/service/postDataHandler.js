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
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    timeZone: 'Asia/Seoul'
  }).format(new Date()); // 한국 시간에 맞게 포맷
}

function processData(postData) {
  // JSON 형식의 게시글 데이터 파싱
  const posts = JSON.parse(postData);

  // 블로그 이름 문자열 생성
  const blogNames = listBlogNames(posts);

  // 본문 마크다운 생성
  const markdownPostsBody = formatPostsToMarkdown(posts);
  
  // Date 객체 생성 및 한국 시간 적용
  const formattedDate = getFormattedDate();

  const issueTitle = `[${formattedDate}] ${blogNames} 블로그 새로운 게시글 업로드`;
  const issueBody = "## 새로운 블로그 게시글 목록\n\n" + markdownPostsBody;
  console.log("-- final Data --")
  console.log(issueTitle)
  console.log(issueBody)

  return { issueTitle, issueBody };
}
 
module.exports = { processData };
  