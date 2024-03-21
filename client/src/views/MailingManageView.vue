<template>
  <v-container>
    <v-row>
      <v-col cols="7">
        <!-- Информация о рассылке -->
        <v-card class="mb-5">
          <v-card-title> Данные рассылки </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="10">
                <v-text-field v-model="selectedMailing.title" label="Тема"></v-text-field>
              </v-col>
            </v-row>
            <v-divider></v-divider>
            <v-row>
              <v-col cols="12">
                <v-textarea v-model="selectedMailing.messagetext" label="Содержимое" rows="5"></v-textarea>
              </v-col>
            </v-row>
            <v-divider></v-divider>
            <v-row>
              <v-col cols="12" class="mt-3">
                <v-btn class="lighten-4 mr-2" color="green" @click="saveMailing">Сохранить</v-btn>
                <v-btn v-if="$route.params.mailingId !== '-1'" color="error" @click="deleteMailing">Удалить</v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Настройки отправки -->
        <v-card class="pref">
          <v-card-title>
            <span class="headline">Настройки отправки</span>
          </v-card-title>
          <v-card-text>
            <v-select v-model="deliveryMethod" :items="deliveryMethods" label="Способ отправки"
              @change="handleDeliveryMethodChange"></v-select>

            <!-- Поля для параметров рассылки для SMTP -->
            <div v-if="deliveryMethod === 'Email'">
              <v-text-field v-model="smtpHost" label="Хост SMTP" autocomplete="on"></v-text-field>
              <v-text-field v-model="smtpPort" label="Порт SMTP" autocomplete="on"></v-text-field>
              <v-text-field v-model="smtpUsername" label="Имя пользователя SMTP" autocomplete="on"></v-text-field>
              <v-row>
                <v-text-field class="ml-3" v-model="smtpPassword" label="Пароль SMTP" :type="passwordType"
                  required autocomplete="on"></v-text-field>
                <v-col cols="2" class="d-flex align-center">
                  <v-btn icon @click="togglePasswordVisibility"
                    :class="{ 'show-password': passwordType === 'password' }">
                    <v-icon>
                      {{ passwordType === 'password' ? 'mdi-eye' : 'mdi-eye-off' }}
                    </v-icon>
                  </v-btn>
                </v-col>
              </v-row>
            </div>

            <!-- Поля для параметров рассылки для Telegram -->
            <div v-else-if="deliveryMethod === 'Telegram'">
              <v-text-field v-model="telegramToken" label="Токен Telegram"></v-text-field>
              <v-text-field v-model="telegramChatId" label="ID чата Telegram"></v-text-field>
            </div>

            <v-btn color="primary" @click="sendMailing">Отправить рассылку</v-btn>
          </v-card-text>
        </v-card>
      </v-col>


      <!-- Показываем получателей в отдельной карточке справа -->
      <v-col cols="5">
        <!-- Верхняя часть для отображения существующих адресов -->
        <v-card class="mb-4">
          <v-card-title>Существующие адреса</v-card-title>
          <v-card-text v-if="isDeliveryMethodSelected" style="max-height: 300px; overflow-y: auto;">
            <v-text-field v-model="searchQuery" label="Поиск адресов" placeholder="Введите адрес для поиска"
              @input="filterAddresses"></v-text-field>
            <v-row justify="start" class="mb-4 ml-4">
              <v-btn class="lighten-4 mr-2" color="orange" @click="selectAllAddresses">{{ selectAllText }}</v-btn>
            </v-row>
            <v-row>
              <v-list dense>
                <v-list-item v-for="(address, index) in shownAddresses" :key="index">
                  <v-row no-gutters v-show="addressMatches(address)">
                    <v-col cols="1" class="px-0 mb-n16">
                      <v-checkbox v-model="selectedAddresses[index]"
                        @change="updateSelectedAddresses(index)"></v-checkbox>
                    </v-col>
                    <v-col cols="auto" class="pl-2">
                      <v-list-item>
                        <v-list-item-title class="ma-0 pa-0">{{ address.address }}</v-list-item-title>
                      </v-list-item>
                    </v-col>
                  </v-row>
                </v-list-item>
              </v-list>
            </v-row>
          </v-card-text>

          <v-card-text v-else>
            <p>Для начала выберите способ отправки.</p>
          </v-card-text>

        </v-card>
        <!-- Нижняя часть для добавления новых адресов -->
        <v-card class="mt-4">
          <v-card-title>Добавление новых адресов</v-card-title>
          <v-card-text v-if="isDeliveryMethodSelected">
            <v-text-field v-model="newAddress" :label="textInputLabel" :rules="textInputRules"></v-text-field>
            <v-btn @click="addNewAddress" :disabled="!isAddressValid">Добавить</v-btn>
          </v-card-text>
        </v-card>
        <v-card class="mt-4">
          <v-card-title>Конечный набор</v-card-title>
          <v-card-text>
            <!-- Вывод выбранных существующих адресов -->
            <v-row v-if="Object.keys(markedAddresses).length > 0">
              <v-col cols="12">
                <strong>Выбранные существующие адреса:</strong>
              </v-col>
              <v-col cols="12">
                <v-list dense>
                  <v-list-item class="mb-n2" v-for="(address, index) in markedAddresses" :key="index">
                    <v-row no-gutters v-if="markedAddresses[index]">
                      <v-col cols="auto">
                        {{ address.address }}
                      </v-col>
                    </v-row>
                  </v-list-item>
                </v-list>
              </v-col>
            </v-row>
            <v-row v-else>
              <v-col cols="12">Нет выбранных существующих адресов.</v-col>
            </v-row>

            <!-- Вывод добавленных новых адресов -->
            <v-row v-if="newAddresses.length > 0">
              <v-col cols="12" class="mt-4">
                <strong>Добавленные новые адреса:</strong>
              </v-col>
              <v-col cols="12">
                <v-list dense>
                  <v-list-item v-for="(address, index) in newAddresses" :key="index">
                    <v-row no-gutters>
                      <v-col cols="auto">
                        {{ address }}
                      </v-col>
                      <v-col class="text-right" cols="auto">
                        <v-icon class="ml-4" @click="removeAddress(index)">mdi-delete</v-icon>
                      </v-col>
                    </v-row>
                  </v-list-item>
                </v-list>
              </v-col>

            </v-row>
            <v-row v-else>
              <v-col cols="12">Нет добавленных новых адресов.</v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Модальное окно для сообщения об ошибке -->
    <v-dialog v-model="errorDialog" max-width="500" persistent>
      <v-card>
        <v-card-title class="headline">Ошибка</v-card-title>
        <v-card-text>{{ errorMessage }}</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red" @click="closeErrorDialog">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>

  <!-- Модальное окно подтверждения удаления -->
  <v-dialog v-model="deleteDialog" max-width="500" persistent>
    <v-card>
      <v-card-title class="headline">Подтверждение удаления</v-card-title>
      <v-card-text>Вы действительно хотите удалить рассылку?</v-card-text>
      <v-card-actions>
        <v-btn color="red darken-1" @click="deleteMailingConfirmed">Да</v-btn>
        <v-btn color="grey" @click="cancelDelete">Отмена</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

</template>

<script>
// Импорт хранилища рассылок из компонента
import { useMailingStore } from '../components/store/mailingStore.js';
import { useAuthStore } from "../components/store/userAuth.js";
import axios from 'axios';

export default {
  // Компонентные данные
  data() {
    return {
      errorDialog: false,
      errorMessage: '',
      deleteDialog: false, // добавляем переменную для управления модальным окном подтверждения удаления
      // Использование хранилища рассылок
      mailingsStore: useMailingStore(),
      // Выбранная рассылка
      selectedMailing: {
        title: '',
        messagetext: '',
        scheduledtime: null
      },
      filteredAddresses: [], //Адреса, отфильтрованные по типу доставки
      deliveryMethod: null,
      // Возможные способы доставки
      deliveryMethods: ['Email', 'Notisend', 'Sendsay', 'Telegram'],
      // Состояние загрузки данных
      searchQuery: '',
      selectedAddresses: [], // Выбранные адреса галочкой в списке адресов
      newAddresses: [],
      newAddress: '',
      markedAddresses: [],
      shownAddresses: [],
      // Параметры рассылки для SMTP
      smtpHost: '',
      smtpPort: '',
      smtpUsername: '',
      smtpPassword: '',
      // Параметры рассылки для Telegram
      telegramToken: '',
      telegramChatId: '',
      passwordType: '',
      allSelected: false
    };
  },
  // Жизненный цикл: создание компонента
  async created() {
    const mailingId = this.$route.params.mailingId;
    // Если индекс -1, это означает, что мы создаем новую рассылку
    if (mailingId === '-1') {
      // Создаем новую рассылку с пустыми значениями
      this.selectedMailing = {
        title: '',
        messagetext: '',
        scheduledtime: null,
      };
    } else {
      // Загружаем рассылку, если индекс не равен -1
      this.loadMailing(mailingId);
    }
  },
  // Вычисляемые свойства компонента
  computed: {
    selectAllText() {
      return this.allSelected ? 'Убрать все' : 'Выбрать все';
    },
    isTelegramDelivery() {
      return this.deliveryMethod === 'Telegram';
    },
    textInputLabel() {
      return this.isTelegramDelivery ? 'Введите новый адрес Telegram' : 'Введите новый Email адрес';
    },
    // Получение списка рассылок из хранилища
    mailings() {
      return this.mailingsStore.mailings;
    },
    isDeliveryMethodSelected() {
      if (!!this.deliveryMethod == true) {
        this.filterAdressesByDeliveryMethod();
      }
      return !!this.deliveryMethod;
    },
    isAddressValid() {
      if (this.isTelegramDelivery) {
        return this.newAddress.startsWith('@') && this.newAddress.length > 1; // Проверка адреса Telegram
      } else {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/; // Полная проверка email адреса
        return emailRegex.test(this.newAddress);
      }
    },
    textInputRules() {
      return [
        value => !!value || 'Поле обязательно для заполнения',
        value => /^[^\s]+$/.test(value) || 'Адрес не должен содержать пробелов',
        value => this.isTelegramDelivery ? (value.startsWith('@') && value.length > 1) || 'Адрес Telegram должен начинаться с "@" и не быть пустым' : /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(value) || 'Введите корректный Email адрес'
      ];
    },
  },
  // Методы компонента
  methods: {
    async filterAdressesByDeliveryMethod() {
      try {
        let response;
        if (this.deliveryMethod === 'Telegram') {
          response = await axios.get(`/addresses/by_type/2`);
        } else {
          response = await axios.get(`/addresses/by_type/1`);
        }
        this.markedAddresses = [];
        this.selectedAddresses = [];
        this.filteredAddresses = response.data;
        this.shownAddresses = response.data;
      } catch (error) {
        console.error('Error filtering adresses:', error);
      }
    },
    addressMatches(address) {
      //возврат списка тех адресов, которые соответствуют поисковому запросу
      return address.address.toLowerCase().includes(this.searchQuery.toLowerCase());
    },
    handleDeliveryMethodChange() {
      // Вызываем фильтрацию адресов при изменении способа доставки
      this.filterAdressesByDeliveryMethod();
    },
    filterAddresses() {
      // В этом методе вы можете фильтровать адреса на основе введенного поискового запроса
      // Например, можно использовать метод filter
      this.shownAddresses = this.filteredAddresses.filter(address => address.address.toLowerCase().includes(this.searchQuery.toLowerCase()));
    },
    showError(message) {
      this.errorMessage = message;
      this.errorDialog = true;
    },
    closeErrorDialog() {
      this.errorDialog = false;
      if (this.errorMessage === 'Рассылка не найдена') {
        // Если сообщение об ошибке содержит "Рассылка не найдена", переадресуем на страницу "Not Found"
        this.$router.push('/not-found');
      }
    },
    // Загрузка данных выбранной рассылки
    async loadMailing(mailingIndex) {
      try {
        // Находим рассылку по индексу в массиве mailings
        const mailing = this.mailings[mailingIndex];
        if (mailing) {
          // Если рассылка найдена, сохраняем её в selectedMailing
          this.selectedMailing = mailing;
        } else {
          console.error('Mailing not found');
          // Если рассылка не найдена, переадресовываем на страницу "Not Found"
          this.showError('Рассылка не найдена');
        }
      } catch (error) {
        console.error('Error fetching mailing:', error);
      }
    },
    // Логика сохранения рассылки
    saveMailing() {
      const authStore = useAuthStore();
      const mailing_Id = this.selectedMailing.mailingid;
      if (this.selectedMailing.title.trim() === '') {
        this.showError('Введите заголовок рассылки');
        return;
      }

      // if (this.selectedMailing.recipients.length === 0) {
      //   this.showError('Выберите хотя бы одного получателя');
      //   return;
      // }

      if (this.selectedMailing.messagetext.trim() === '') {
        this.showError('Введите текст сообщения');
        return;
      }
      try {
        // Если у рассылки есть id, значит она уже существует и нужно обновить её
        if (this.$route.params.mailingId != '-1') {
          // Логика обновления рассылки
          this.mailingsStore.updateMailing(mailing_Id, authStore.user.user_data.id, this.selectedMailing);
        }
        else {
          // Если у рассылки нет id, значит это новая рассылка и нужно добавить её
          // Логика добавления новой рассылки
          this.mailingsStore.createMailing(this.selectedMailing, authStore.user.user_data.id);
        }
        this.$router.push('/mailings'); // Переход на страницу списка рассылок после сохранения
      }
      catch (error) {
        console.error('Error saving mailing:', error);
        this.showError('Произошла ошибка при сохранении рассылки');
      }
    },
    // Логика удаления рассылки
    deleteMailing() {
      // Открываем модальное окно подтверждения удаления
      this.deleteDialog = true;
    },
    deleteMailingConfirmed() {
      // Вызываем логику удаления рассылки только после подтверждения
      this.deleteDialog = false; // закрываем модальное окно
      const authStore = useAuthStore();
      const mailing_Id = this.selectedMailing.mailingid;
      try {
        // Отправляем запрос на сервер для удаления рассылки по ее идентификатору
        this.mailingsStore.deleteMailing(mailing_Id, authStore.user.user_data.id);
        this.$router.push('/mailings');
      } catch (error) {
        console.error('Error deleting mailing:', error);
        this.showError('Произошла ошибка при удалении рассылки');
      }
    },
    cancelDelete() {
      // Отменяем удаление рассылки и закрываем модальное окно
      this.deleteDialog = false;
    },
    // Логика отправки рассылки
    sendMailing() {
      // Логика отправки рассылки
      // const adressesForMailing = this.markedAddresses.concat(this.newAddresses);

      //в markedAddresses хранятся объекты (id, type_id, address), в newAddresses только address
      //берём только адреса получателей      
      const recipient_emails = this.markedAddresses.map(item => item.address).concat(this.newAddresses);

      const formData = {
        recipient_emails: recipient_emails, // список адресов получателей
        subject: this.selectedMailing.title, // тема письма
        body: this.selectedMailing.messagetext, // текст сообщения
        smtp_host: this.smtpHost, // хост SMTP-сервера
        smtp_port: this.smtpPort, // порт SMTP-сервера
        smtp_username: this.smtpUsername, // имя пользователя SMTP
        smtp_password: this.smtpPassword // пароль SMTP
      };

      // Отправляем POST-запрос на бэкенд
      axios.post('/send_email', formData)
        .then(response => {
          console.log(response.data); // Выводим ответ от сервера в консоль
          // Добавьте здесь код для обработки успешного ответа от сервера
        })
        .catch(error => {
          console.error('Error sending email:', error); // Обработка ошибки при отправке запроса
          // Добавьте здесь код для обработки ошибки при отправке запроса
          if (error.isAxiosError) {
            // Данные запроса можно найти в свойстве config
            if (error.config && error.config.data) {
              const requestData = JSON.parse(error.config.data);
              console.log("Данные запроса:", requestData);
            } else {
              console.log("Данные запроса отсутствуют");
            }
          } else {
            console.error("Ошибка не является объектом AxiosError");
          }

        });
    },
    // Метод для добавления нового адреса
    addNewAddress() {
      // Проверяем, существует ли адрес в атрибуте address объектов filteredAddresses
      if (this.filteredAddresses.some(item => item.address === this.newAddress)) {
        this.showError('Этот адрес есть в списке существующих');
        return;
      }
      if (this.newAddresses.includes(this.newAddress)) {
        this.showError('Этот адрес уже есть в списке');
        return;
      }
      if (this.newAddress.trim() !== '') {
        this.newAddresses.push(this.newAddress.trim());
        this.newAddress = ''; // Очищаем поле ввода
      }
    },
    removeAddress(index) {
      this.newAddresses.splice(index, 1);
    },
    updateSelectedAddresses(index) {
      if (this.selectedAddresses[index]) {
        // если адрес отмечен, добавить его в массив
        // например, используем метод push
        this.markedAddresses.push(this.shownAddresses[index]);
        if(this.selectedAddresses.length === this.shownAddresses.length) {
          this.allSelected = true;
        }
      } else {
        // если адрес снят, удалить его из массива
        // например, используем метод splice
        const selectedIndex = this.markedAddresses.indexOf(this.shownAddresses[index]);
        if (selectedIndex !== -1) {
          this.markedAddresses.splice(selectedIndex, 1);
        }
      }
    },
    selectAllAddresses() {
      this.allSelected = !this.allSelected;
      // Проверяем, все ли чекбоксы уже установлены в true
      const allSelected = this.selectedAddresses.every(selected => selected);

      if (allSelected && this.selectedAddresses.length > 0) {
        // Если все чекбоксы уже установлены в true, снимаем все галочки
        this.selectedAddresses = this.shownAddresses.map(() => false);
        this.markedAddresses = [];
      } else {
        // Если хотя бы один чекбокс не установлен в true, выбираем все адреса и добавляем их в массив отмеченных адресов
        this.selectedAddresses = this.shownAddresses.map(() => true);
        this.markedAddresses = [...this.shownAddresses];
      }
    },
    togglePasswordVisibility() {
      this.passwordType = this.passwordType === "password" ? "text" : "password";
    }
  }
};
</script>

<style>
.v-card.mb-4 {
  border: 2px solid #eea215;
  /* Цвет рамки */
  border-radius: 10px;
  /* Закругление углов */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  /* Тень */
}

.v-card.mb-5 {
  border: 2px solid #98ac28;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.v-card.mt-4 {
  border: 2px solid #1530a8;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.v-card.pref {
  border: 2px solid #000000;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}
</style>