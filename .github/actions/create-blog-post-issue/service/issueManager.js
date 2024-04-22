const core = require('@actions/core');
const github = require('@actions/github');

async function createIssue(token, issueTitle, issueBody) {
  try {
    const octokit = github.getOctokit(token);
    const { repo, owner } = github.context.repo;
    const response = await octokit.rest.issues.create({
      owner,
      repo,
      title: issueTitle,
      body: issueBody
    });
    core.setOutput("issue-url", response.data.html_url);
  } catch (error) {
    core.setFailed(`Issue creation failed with error: ${error}`);
  }
}

module.exports = { createIssue };
