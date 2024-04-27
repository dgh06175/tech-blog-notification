const core = require('@actions/core');
const { createIssue } = require('./service/issueManager');
const { formatBlogMarkdown } = require('./service/articleDataHandler')

async function run() {
  try {
    const token = core.getInput('GITHUB_TOKEN', { required: true });
    const { issueTitle, issueBody } = await formatBlogMarkdown();

    await createIssue(token, issueTitle, issueBody);
  } catch (error) {
    core.setFailed(`액션 실패: ${error}`);
  }
}

run();
