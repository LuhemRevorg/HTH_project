const path = require('path');

module.exports = {
  mode: 'development', // or 'production'
  entry: './src/index.js', // adjust this to your entry point
  output: {
    path: path.resolve(__dirname, 'dist'), // output directory
    filename: 'bundle.js', // output bundle filename
    publicPath: '/', // base path for your assets
  },
  module: {
    rules: [
      {
        test: /\.js$/, // process JavaScript files
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader', // use Babel for transpiling
        },
      },
      {
        test: /\.css$/, // process CSS files
        use: ['style-loader', 'css-loader'], // load CSS
      },
      // add other loaders as needed
    ],
  },
  resolve: {
    fallback: {
      stream: require.resolve('stream-browserify'), // polyfill for stream
      // add other fallbacks here as needed
    },
  },
  devtool: 'source-map', // enable source maps for easier debugging
  devServer: {
    contentBase: path.join(__dirname, 'dist'), // serve content from the dist directory
    compress: true, // enable gzip compression
    port: 9000, // port number for the dev server
  },
};
