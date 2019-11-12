const ghpages = require('gh-pages')

// replace with your repo url
ghpages.publish(
  'public',
  {
    // branch: 'docs',
    // repo: 'https://github.com/remorses/flexdinesh.github.io.git',
  },
  () => {
    console.log('Deploy Complete!')
  }
)