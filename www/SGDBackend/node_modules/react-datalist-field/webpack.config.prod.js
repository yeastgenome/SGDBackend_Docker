let merge = require('webpack-merge');
let base = require('./webpack.config.base');
var path = require('path');

let prod = {
  mode:'production',
  output: {
    path: path.resolve(__dirname),
    filename: 'index.js',
    libraryTarget: 'commonjs2',
    library:'react-datalist-field'
  },
  externals: {
    'react': 'commonjs react' 
  }
}

module.exports = merge(base,prod);