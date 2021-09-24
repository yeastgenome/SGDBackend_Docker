let merge = require('webpack-merge');
let base = require('./webpack.config.base');
var path = require('path');

let dev = {
  mode:'development',
  devtool:'source-map',
  output: {
    path: path.resolve(__dirname, 'build'),
    filename: 'index.js',
    library:'react_datalist_field'
  },
  devServer:{
    contentBase:path.join(__dirname,'build'),
    port:9000,
    open:false
  }
}

module.exports = merge(base,dev);