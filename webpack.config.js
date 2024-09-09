const { watch } = require("fs");
const path = require("path");
const TerserPlugin = require("terser-webpack-plugin");


module.exports = {
    watch: true,
    entry: {
        main: "./app/static/js/index.js",
        cryptoList0: "./app/static/js/cryptoList0.js",
        profile: "./app/static/js/profile.js",
        cryptocurrency: "./app/static/js/cryptocurrency.js",
    },
    output: {
        path: path.resolve(__dirname, "./app/static/js/"),
        filename: "[name].min.js",
    },
    resolve: {
        extensions: [".js"],
    },
    // module: {
    //     rules: [
    //         {
    //             test: /\.ts$/,
    //             use: "ts-loader",
    //             exclude: /node_modules/,
    //         },
    //     ],
    // },
    optimization: {
        minimize: false,
        minimizer: [new TerserPlugin()],
    },
    mode: "production",
};