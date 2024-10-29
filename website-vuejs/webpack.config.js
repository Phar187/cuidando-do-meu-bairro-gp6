module.exports = {
    resolve: {
        // ... rest of the resolve config
        fallback: {
          "util": require.resolve("util/")
        }
    },
}
