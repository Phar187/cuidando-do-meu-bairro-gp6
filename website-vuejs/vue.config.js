module.exports = {
  publicPath: process.env.CI_PROJECT_NAME ? `/${process.env.CI_PROJECT_NAME}/` : '/',
  pluginOptions: {
    i18n: {
      locale: 'pt-br',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableInSFC: true
    }
  }
}
