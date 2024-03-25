<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card>
          <v-card-title class="headline grey lighten-2">
            Регистрация
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="submitRegistrationDetails">
              <v-text-field v-model="username" label="Введите имя пользователя" required
                @blur="errorUsername = ''"></v-text-field>
              <v-row>
                <v-col cols="12">
                  <v-text-field v-model="email" label="Введите электронную почту" required :rules="emailRules"
                    @blur="errorEmail = ''"></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-divider></v-divider>
              </v-row>
              <v-row>
                <v-col cols="10">
                  <v-text-field v-model="password" label="Введите пароль" :type="passwordType" required
                    @blur="errorPassword = ''"></v-text-field>
                </v-col>
                <v-col cols="2" class="d-flex align-center">
                  <v-btn icon @click="togglePasswordVisibility"
                    :class="{ 'show-password': passwordType === 'password' }">
                    <v-icon>
                      {{ passwordType === 'password' ? 'mdi-eye' : 'mdi-eye-off' }}
                    </v-icon>
                  </v-btn>
                </v-col>
              </v-row>
              <v-text-field v-model="passwordConfirmation" label="Подтвердите пароль" :type="passwordType" required
                @blur="errorPassword = ''"></v-text-field>
              <v-alert v-if="errorRegister" type="error" dismissible>
                {{ errorRegister }}
              </v-alert>
              <v-btn color="primary" type="submit" block>Зарегистрироваться</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, watch } from "vue";
import { useAuthStore } from "../components/store/userAuth.js";
import { storeToRefs } from "pinia";

const authStore = useAuthStore();
// pulling registration error from backend
const { errorRegister } = storeToRefs(authStore);
const email = ref("");
const emailRegEx =
  /^(([^<>()\]\\.,;:\s@"]+(\.[^<>()\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,24}))$/;

const errorEmail = ref("");
const errorUsername = ref("");
const errorPassword = ref("");

const username = ref("");
const password = ref("");
const passwordConfirmation = ref("");
const passwordType = ref("password");
const passwordsMatch = ref(false);

function togglePasswordVisibility() {
  passwordType.value = passwordType.value === 'password' ? 'text' : 'password';
}

async function submitRegistrationDetails() {
  // validate email
  if (email.value === null || email.value === "") {
    errorEmail.value = "Please Enter Email";
  } else if (!emailRegEx.test(email.value)) {
    errorEmail.value = "Please Enter Valid Email";
  } else {
    errorEmail.value = "";
  }

  // validate username
  if (username.value === "") {
    errorUsername.value = "Please Enter Username";
  } else {
    errorUsername.value = "";
  }

  // validate passwords match
  if (password.value === "" || passwordConfirmation.value === "") {
    errorPassword.value = "Please Enter Password";
  } else if (password.value !== passwordConfirmation.value) {
    errorPassword.value = "Passwords do not match";
  } else {
    errorPassword.value = "";
  }

  // checking all errors at once
  let errorsArray = [
    errorUsername.value,
    errorEmail.value,
    errorPassword.value,
  ];
  const checker = (arr) => arr.every((arr) => arr === "");

  if (checker(errorsArray)) {
    const payload = {
      name: username.value,
      email: email.value,
      password: password.value,
      roleid: 1,
    };
    authStore.register(payload);
  }
}

// Clear error from backend if any of the inputs change
watch([username, email, password, passwordConfirmation], () => {
  errorRegister.value = false;
});

watch([password, passwordConfirmation], () => {
  if (passwordConfirmation.value !== password.value) {
    passwordsMatch.value = false;
  } else {
    passwordsMatch.value = true;
  }
});
</script>