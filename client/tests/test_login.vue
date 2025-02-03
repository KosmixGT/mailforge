import { mount } from '@vue/test-utils'
import LoginView from '@/views/LoginView.vue'
import { createStore } from 'vuex'

describe('Login Integration', () => {
  it('should login user and redirect to dashboard', async () => {
    const store = createStore({
      modules: {
        auth: {
          actions: {
            login: jest.fn().mockResolvedValue(true)
          }
        }
      }
    })

    const wrapper = mount(LoginView, {
      global: {
        plugins: [store]
      }
    })

    await wrapper.find('input[type="email"]').setValue('test@test.com')
    await wrapper.find('input[type="password"]').setValue('test123')
    await wrapper.find('form').trigger('submit')

    expect(store.state.auth.isAuthenticated).toBe(true)
  })
})
