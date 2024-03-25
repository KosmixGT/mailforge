import { defineStore } from "pinia";
import axios from "axios";
import router from "../../router.js";

export const useAuthStore = defineStore("authentication", {
  state: () => ({
    token: "",
    // initialize state from local storage to enable user to stay logged in
    user: JSON.parse(localStorage.getItem("user")),
    errorLogIn: false,
    errorMessage: "",
    isAuthenticated: false,
    errorRegister: false,
  }),
  actions: {
    initialize() {
      const user = JSON.parse(localStorage.getItem('user'));
      if (user && user.access_token) {
        this.token = user.access_token;
        this.isAuthenticated = true;
      }
    },
    async login(username, password) {
      const params = new URLSearchParams();
      params.append("username", username);
      params.append("password", password);

      const headers = {
        Accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
      };
      await axios
        .post("user/jwt/create/", params, {
          headers: headers,
        })
        .then((response) => {
          // store user details and jwt in local storage to keep user logged in between page refreshes
          localStorage.setItem("user", JSON.stringify(response.data));
          this.user = JSON.parse(localStorage.getItem('user'));
          // update pinia state
          this.token = response.data["access_token"];
          this.isAuthenticated = true;
          //чтобы не вылетала ошибка сразу после логина
          this.user = JSON.parse(localStorage.getItem('user'));
          router.push({ name: "Home" });
          window.location.reload();
        })
        .catch((error) => {
          console.log(error);
          this.errorLogIn = true;
          // catching connection refused error
          if (error.message === "Network Error") {
            this.errorMessage = error.message;
          } else {
            this.errorMessage = "Incorrect username/email or password";
          }
        });
    },
    async register(payload) {
      await axios
        .post("users/register/", payload, {
          headers: {
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          router.push({ name: "Authorization" });
          console.log(
            `User ${response.data.username} has been successfully created!`
          );
        })
        .catch((error) => {
          console.log(error);
          this.errorRegister = error.response.data.detail;
        });
    },
    logout() {
      localStorage.clear();
      router.push('/');
      setTimeout(() => {
        window.location.reload();
      }, 100);
      // router.push('/');
      // this.token = null;
      // localStorage.removeItem("user");
      // localStorage.removeItem("user_data");
      // localStorage.removeItem("mailings");
      // this.isAuthenticated = false;
      // window.location.reload();
    },

    async refreshToken() {
      var user = localStorage.getItem("user");
      user = JSON.parse(user);
      const refresh = user["refresh_token"];
      localStorage.removeItem("user");

      const refreshToken = await axios.post("user/jwt/refresh/", {
        refresh: refresh,
      });
      // reassign user in local storage
      user["access_token"] = refreshToken.data.access;
      localStorage.setItem("user", JSON.stringify(user));
      return refreshToken.data.access;
    },

    clearError() {
      this.errorLogIn = false;
    },
  },
});