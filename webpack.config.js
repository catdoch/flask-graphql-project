const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    entry: ['./client/src/index.jsx'],
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
        path: __dirname + '/static',
        filename: 'bundle.js',
    },
};
