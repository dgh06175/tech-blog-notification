const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    // GitHub 토큰과 포스트 데이터 가져오기
    const token = core.getInput('GITHUB_TOKEN', { required: true });
    const postData = core.getInput('POST_DATA', { required: true });
    const posts = JSON.parse(postData);

    // Octokit 객체 초기화
    const octokit = github.getOctokit(token);

    // Date 객체 생성 및 한국 시간 적용
    const currentDate = new Date();
    const kstOffset = 9 * 60 * 60 * 1000; // 한국 시간에 맞게 UTC 기준 시간에 9시간 추가 (밀리초 단위)
    const kstDate = new Date(currentDate.getTime() + kstOffset);
    const formattedDate = `${kstDate.getFullYear()}.${kstDate.getMonth() + 1}.${kstDate.getDate()}`; // 한국 시간에 맞게 포맷

    // 포스트 데이터 파싱
    // const posts = parsingPostData(postData)
    
    console.log("-- postData --")
    console.log(postData)
    console.log("-- posts --")
    console.log(posts);

    const markdownPosts = formatPostsToMarkdown(posts)

    // 이슈 생성
    const { repo, owner } = github.context.repo;
    const issueTitle = `새로운 블로그 게시글이 올라왔습니다. [${formattedDate}]`;
    const issueBody = "## 새로운 블로그 게시글 목록\n\n" + markdownPosts;

    const response = await octokit.rest.issues.create({
      owner,
      repo,
      title: issueTitle,
      body: issueBody
    });

    core.setOutput("issue-url", response.data.html_url);
  } catch (error) {
    core.setFailed(`Action failed with error: ${error}`);
  }
}

/// MARK: 파이썬에서 받아온 문자열 데이터를 객체로 바꾸는 함수.
/// 문자열은 다음과 같이 넘어온다.
/// f"{blog_name}||{latest_post_info['title']}||{latest_post_info['link']}"
function parsingPostData(stringPostData) {
  const postLines = stringPostData.trim().split('::'); // 데이터 분리 (여러개일 경우)
    const posts = postLines.map(line => {
      const parts = line.split('||');
      if (parts.length === 3) { // 정확히 세 부분이 있는지 확인
        return {
          blogName: parts[0].trim(),
          title: parts[1].trim(),
          link: parts[2].trim()
        };
      } else {
        console.error('Invalid post data:', line);
        return null; // 오류 처리
      }
    }).filter(post => post !== null); // null이 아닌 객체만 필터링
    return posts
}

/// MARK: posts 객체 배열을 마크다운으로 바꾸는 함수
function formatPostsToMarkdown(posts) {
  return posts.map(post => {
    return `### ${post.blogName}\n\n[${post.title}](${post.link})\n`;
  }).join('\n');
}

run();