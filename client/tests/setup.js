const { config } = require('@vue/test-utils')
const { createVuetify } = require('vuetify')

const vuetify = createVuetify()
config.global.plugins = [vuetify]
