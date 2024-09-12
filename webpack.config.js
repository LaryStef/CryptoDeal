const path = require("path");
const TerserPlugin = require("terser-webpack-plugin");


module.exports = {
    //watch: true,
    entry: {
        index: "./frontend/js/index.js",
        cryptoList: "./frontend/js/cryptoList.js",
        profile: "./frontend/js/profile.js",
        cryptocurrency: "./frontend/js/cryptocurrency.js"
    },
    output: {
        path: path.resolve(__dirname, "./app/static/js/"),
        filename: "[name].min.js"
    },
    resolve: {
        extensions: [".js"],
    },
    optimization: {
        minimize: true,
        minimizer: [new TerserPlugin()],
    },
    mode: "production",
};
