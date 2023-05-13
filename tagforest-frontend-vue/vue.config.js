module.exports = {
  pages: {
    index: {
      entry: 'src/main.js',
      template: 'public/index.html',
      filename: 'index.html',
      title: 'Tagforest',
      chunks: ['chunk-vendors', 'chunk-common', 'index']
    },
  }
}
