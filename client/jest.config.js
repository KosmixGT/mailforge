module.exports = {
    moduleFileExtensions: ['js', 'json', 'vue'],
    transform: {
      '^.+\\.vue$': '@vue/vue3-jest',
      '^.+\\.js$': 'babel-jest'
    },
    moduleNameMapper: {
      '^@/(.*)$': '<rootDir>/src/$1',
      '^vuetify$': 'vuetify/dist/vuetify.js'
    },
    testEnvironment: 'jsdom',
    transformIgnorePatterns: [
      'node_modules/(?!(axios|vuetify)/)'
    ],
    setupFiles: ['<rootDir>/tests/setup.js'],
    testEnvironmentOptions: {
      customExportConditions: ["node", "node-addons"],
    }
  }
  