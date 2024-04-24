const core = require('@actions/core');
const { processData } = require('../create-blog-post-issue/service/postDataHandler');

async function run_test() {
  const postData = core.getInput('POST_DATA', { required: true });
  console.log("수신한 데이터: ")
  console.log(postData)
  // const { issueTitle, issueBody } = processData(postData);
}

run_test();
