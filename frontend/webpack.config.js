const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    mode: "development",
    devtool: "inline-source-map",
    entry: {index: "./src/index.tsx"},
    output: {
        filename: "[name].js",
        path: path.resolve(__dirname, "dist"),
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                exclude: /node_modules/,
                loader: "ts-loader"
            },
            {
                test: /\.css$/i,
                use: [MiniCssExtractPlugin.loader, "css-loader", "postcss-loader"],
            },
        ]
    },
    resolve: {
        extensions: [".tsx", ".ts", ".js", ".css", "..."],
    },
    plugins: [
        new MiniCssExtractPlugin({}),
    ],
};