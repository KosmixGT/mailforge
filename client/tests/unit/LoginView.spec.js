const LoginView = require('@/views/LoginView.vue')

describe('LoginView.vue', () => {
  it('component can be imported', () => {
    expect(LoginView).toBeTruthy()
  })

  it('has correct default export structure', () => {
    expect(LoginView.default).toHaveProperty('data')
    expect(LoginView.default).toHaveProperty('methods')
    expect(LoginView.default).toHaveProperty('computed')
  })

  it('contains required method names', () => {
    const methodNames = Object.keys(LoginView.default.methods)
    expect(methodNames).toContain('submitLogDetails')
    expect(methodNames).toContain('togglePasswordVisibility')
    expect(methodNames).toContain('clearError')
  })
})
