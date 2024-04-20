const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    // GitHub 토큰과 포스트 데이터 가져오기
    const token = core.getInput('GITHUB_TOKEN', { required: true });
    const postData = core.getInput('POST_DATA', { required: true });

    // Octokit 객체 초기화
    const octokit = github.getOctokit(token);

    // 이슈 생성
    const { repo, owner } = github.context.repo;
    const issueTitle = '새로운 블로그 게시글이 올라왔습니다!';
    const issueBody = `## 새로운 블로그 게시글 목록\n\n${postData.replace(/::/g, '\n')}`;

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
