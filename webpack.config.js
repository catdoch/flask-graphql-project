const MiniCssExtractPlugin = require('mini-css-extract-plugin');
//const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

module.exports = {
    entry: ['./app/client/src/index.js'],
    devtool: 'source-map',
    module: {
        rules: [
            {
                test: /\.(ts|js)x?$/,
                exclude: /(node_modules)/,
                use: {
                    loader: 'babel-loader',
                },
            },
            {
                test: [/.css$|.scss$/],
                use: ['style-loader', 'css-loader', 'sass-loader'],
            },
        ],
    },
    plugins: [
        new MiniCssExtractPlugin({
            // Options similar to the same options in webpackOptions.output
            // both options are optional
            filename: '[name].css',
            chunkFilename: '[id].css',
        }),
    ],
    output: {
        path: __dirname + '/app/static',
        filename: 'bundle.js',
    },
    // optimization: {
    //     concatenateModules: true,
    //     minimizer: [new UglifyJsPlugin()],
    // },
};
