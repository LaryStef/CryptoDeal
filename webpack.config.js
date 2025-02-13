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
        indexStyles: "./frontend/scss/compile/indexStyles.js",
        cryptoListStyles: "./frontend/scss/compile/cryptoListStyles.js",
        cryptocurrencyStyles: "./frontend/scss/compile/cryptocurrencyStyles.js",
        profileStyles: "./frontend/scss/compile/profileStyles.js",
        notFoundStyles: "./frontend/scss/compile/notFoundStyles.js",
        securitiesStyles: "./frontend/scss/compile/securitiesStyles.js",
        aboutStyles: "./frontend/scss/compile/aboutStyles.js",
        newsStyles: "./frontend/scss/compile/newsStyles.js",
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
            use: [
                MiniCssExtractPlugin.loader,
                "css-loader",
                {
                    loader: "postcss-loader",
                    options: {
                        postcssOptions: {
                            plugins: [
                                [
                                    "autoprefixer",
                                    {
                                        "overrideBrowserslist": [
                                            "last 5 versions",
                                            "> 1%",
                                            "IE >= 10",
                                            "Firefox >= 30",
                                            "Chrome >= 30",
                                            "Safari >= 7",
                                            "iOS >= 7",
                                            "Android >= 4.4"
                                        ],
                                    },
                                ],
                            ],
                        },
                    },
                },
                "sass-loader",
            ],
        },
      ],
    },
    optimization: {
        minimize: true,
        minimizer: [new TerserPlugin({
            "extractComments": false,
        })],
    },
    mode: "production",
};
