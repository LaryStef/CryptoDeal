const { watch } = require("fs");
const path = require("path");
const TerserPlugin = require("terser-webpack-plugin");


module.exports = {
    watch: true,
    entry: {
        index: "./app/static/js/index.js",
        cryptoList: "./app/static/js/cryptoList.js",
        profile: "./app/static/js/profile.js",
        cryptocurrency: "./app/static/js/cryptocurrency.js"
    },
    output: {
        path: path.resolve(__dirname, "./app/static/js/"),
        filename: "[name].min.js",
    },
    resolve: {
        extensions: [".js"],
    },
    optimization: {
        minimize: false,
        minimizer: [new TerserPlugin()],
    },
    mode: "production",
};
