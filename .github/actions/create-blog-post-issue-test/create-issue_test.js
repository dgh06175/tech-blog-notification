const core = require('@actions/core');
const { processData } = require('../create-blog-post-issue/service/postDataHandler');

async function run_test() {
  const postData = core.getInput('POST_DATA', { required: true });
  const { issueTitle, issueBody } = processData(postData);
}

run_test();
