module.exports = {
  mode: "production",
  entry: "./receiver.js",
  experiments: { asyncWebAssembly: true, outputModule: true },
  output: { module: true, library: { type: "module" }, path: __dirname + "/dist", filename: "receiver.js" },
};
