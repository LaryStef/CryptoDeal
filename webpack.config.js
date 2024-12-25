const path = require("path");
const TerserPlugin = require("terser-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");


module.exports = {
    watch: true,
    entry: {
        cryptoList: "./frontend/js/cryptoList.js",
        index: "./frontend/js/index.js",
        profile: "./frontend/js/profile.js",
        cryptocurrency: "./frontend/js/cryptocurrency.js",
        indexStyles: "./frontend/js/indexStyles.js",
        cryptoListStyles: "./frontend/js/cryptoListStyles.js",
        cryptocurrencyStyles: "./frontend/js/cryptocurrencyStyles.js",
        profileStyles: "./frontend/js/profileStyles.js",
    },
    output: {
        path: path.resolve(__dirname, "./app/static"),
        filename: "./js/[name].min.js"
    },
    resolve: {
        extensions: [".js"],
    },
    plugins: [new MiniCssExtractPlugin({
        filename: "css/[name].min.css",
    })],
    module: {
      rules: [
        {
            test: /\.s[ac]ss$/i,
          use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
        },
      ],
    },
    optimization: {
        minimize: true,
        minimizer: [new TerserPlugin({
            "extractComments": false,
        })],
    },
    mode: "development",
};
