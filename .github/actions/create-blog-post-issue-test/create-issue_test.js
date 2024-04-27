// const core = require('@actions/core');
const { formatBlogMarkdown } = require('./service/articleDataHandler')

async function run() {
  const { issueTitle, issueBody } = await formatBlogMarkdown();
  console.log("!issueTitle")
  console.log(issueTitle)
  console.log("!issueBody")
  console.log(issueBody)
}

run()