<template>
  <h1>История отправленных рассылок</h1>
  <v-alert v-if="histories.length === 0" value="true" type="info">
    История рассылок пуста.
  </v-alert>
  <v-progress-linear v-if="loading" indeterminate color="primary"></v-progress-linear>
  <v-container>
    <v-row>
      <v-col cols="3" v-for="history in histories" :key="history.historyid">
        <v-card class="mb-5">
          <v-card-title>{{ new Date(history.senttime).toLocaleString() }}</v-card-title>
          <v-card-text>
            <!-- тема рассылки ищется по атрибуту id рассылки в массиве рассылок-->
            <div>Тема рассылки: {{ mailingsStore.mailings.find(mailing => mailing.mailingid === history.mailingid).title
              }}</div>
            <div>Статус: {{ history.deliverystatusid === 1 ? 'Доставлено' : 'Не доставлено' }}</div>
            <!-- Добавьте другие поля, которые хотите отображать -->
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn color="primary" @click="viewRecipients(history.historyid)">Посмотреть получателей</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалоговое окно для отображения получателей -->
    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>Список получателей</v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item v-for="recipient in recipients" :key="recipient.recipientid">
              <v-list-item-title>{{ recipient.address }}</v-list-item-title>
              <v-list-item-subtitle>{{ recipient.status === 1 ? 'Доставлено' : 'Не доставлено' }}</v-list-item-subtitle>
              <!-- Добавьте другие поля, которые хотите отобразить для каждого получателя -->
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="dialog = false">Закрыть</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { useAuthStore } from "../components/store/userAuth.js";
import { useMailingStore } from '../components/store/mailingStore.js';
import axios from 'axios';

export default {
  data() {
    return {
      mailingsStore: useMailingStore(),
      histories: [], // Массив для хранения истории рассылок
      dialog: false, // Переменная для управления отображением диалогового окна
      recipients: [], // Массив для хранения получателей
    }
  },
  async created() {
    const authStore = useAuthStore();
    this.loading = true; // Устанавливаем состояние загрузки в true перед запросом данных
    try {
      const savedMailings = JSON.parse(localStorage.getItem('mailings'));
      if (savedMailings) {
        this.mailingsStore.mailings = savedMailings;
        // console.log("Загрузка сохр рассылок")
      } else {
        await this.mailingsStore.fetchMailingsByUserId(authStore.user.user_data.id);
        localStorage.setItem('mailings', JSON.stringify(this.mailingsStore.mailings));
        // console.log("Полная загрузка рассылок с запросом к БД")
      }
    } catch (error) {
      console.error('Ошибка загрузки рассылок:', error);
    } finally {
      this.loading = false; // После завершения запроса устанавливаем состояние загрузки в false
    }
  },
  methods: {
    // Метод для загрузки истории рассылок из API
    loadHistory() {
      const authStore = useAuthStore();
      // Загрузка истории рассылок из API
      axios.get(`/history/by_user/${authStore.user.user_data.id}`)
        .then(response => {
          this.histories = response.data.reverse();
        })
        .catch(error => {
          console.error(error);
        });
    },
    // Метод для загрузки получателей по идентификатору записи истории
    viewRecipients(historyId) {
      this.recipients = []
      // Загрузка получателей из API по идентификатору записи истории
      axios.get(`/recipients/load_recipients/${historyId}`)
        .then(response => {
          console.log("Получатели по id истории:", response.data);
          for (const recipient of response.data) {
            axios.get(`/addresses/${recipient.addressid}`)
              .then(response => {
                console.log("адреса: ", response.data);
                const recip = {
                  status: recipient.deliverystatusid,
                  address: response.data.address
                }
                this.recipients.push(recip)
              })
              .catch(error => {
                console.error(error);
              });
          }
          console.log("получатели: ", this.recipients);
          this.dialog = true;
        }
        )
        .catch(error => {
          console.error(error);
        });
    }
  },
  mounted() {
    // При монтировании компонента загружаем историю рассылок
    this.loadHistory();
  }
}
</script>

<style>
/* CSS стилизация, если необходимо */
.v-card.mb-5 {
  border: 2px solid #98ac28;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
