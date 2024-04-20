const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    // GitHub 토큰과 포스트 데이터 가져오기
    const token = core.getInput('GITHUB_TOKEN', { required: true });
    const postData = core.getInput('POST_DATA', { required: true });

    // Octokit 객체 초기화
    const octokit = github.getOctokit(token);

    // Date 객체 생성 및 한국 시간 적용
    const currentDate = new Date();
    const kstOffset = 9 * 60 * 60 * 1000; // 한국 시간에 맞게 UTC 기준 시간에 9시간 추가 (밀리초 단위)
    const kstDate = new Date(currentDate.getTime() + kstOffset);
    const formattedDate = `${kstDate.getFullYear()}.${kstDate.getMonth() + 1}.${kstDate.getDate()}`; // 한국 시간에 맞게 포맷

    // 이슈 생성
    const { repo, owner } = github.context.repo;
    const issueTitle = `새로운 블로그 게시글이 올라왔습니다. [${formattedDate}]`;
    const issueBody = `## 새로운 블로그 게시글 목록\n\n${postData.replace(/::/g, '\n')}`;

    console.log(postData)

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

run();
