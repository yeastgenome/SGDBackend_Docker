var path = require('path');
module.exports = {
  entry: './src/index.js',
  target:'node',
  module: {
    rules: [
      {
        test: /\.js$/,
        include: path.resolve(__dirname, 'src'),
        exclude: /(node_modules|bower_components|build)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
      {
        test:/\.css$/,
        include: path.resolve(__dirname, 'src'),
        use: ['style-loader','css-loader'],
      }
    ]
  }
};