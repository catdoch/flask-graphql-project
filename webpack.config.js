module.exports = {
  entry: [
      './client/src/index.jsx'
  ],
  devtool: 'source-map',
  module: {
      rules: [
          {
              test: /\.(js|jsx)$/,
              exclude: /node_modules/,
              use: ['babel-loader']
          }
      ]
  },
  output: {
      path: __dirname + '/static',
      filename: 'bundle.js'
  }
};