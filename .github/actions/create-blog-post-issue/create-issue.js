const core = require('@actions/core');
const { createIssue } = require('./service/issueManager');
const { processData } = require('./service/postDataHandler');

async function run() {
  try {
    const token = core.getInput('GITHUB_TOKEN', { required: true });
    const postData = core.getInput('POST_DATA', { required: true });

    const { issueTitle, issueBody } = processData(postData);

    await createIssue(token, issueTitle, issueBody);
  } catch (error) {
    core.setFailed(`Action failed with error: ${error}`);
  }
}

run();
