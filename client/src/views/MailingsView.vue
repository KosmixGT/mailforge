<template>
  <v-container>
    <v-row align="center">
      <v-col cols="auto">
        <v-btn color="light-green darken-3" @click="createMailing" class="btn-style">Создать рассылку</v-btn>
        <v-btn color="primary" @click="openFileDialog" class="btn-style ml-5">
          <v-icon left>mdi-upload</v-icon> Загрузить рассылки (Excel/CSV)
        </v-btn>
      </v-col>
      <v-col cols="4">
        <h1>Список рассылок</h1>
      </v-col>
      <v-col cols="12">
        <v-text-field v-model="searchQuery" label="Поиск по названию рассылки" outlined clearable></v-text-field>
      </v-col>
    </v-row>
    <v-progress-linear v-if="loading" indeterminate color="primary"></v-progress-linear>
    <div v-else>
      <v-alert v-if="mailings.length === 0" value="true" type="info">
        Нет доступных рассылок.
      </v-alert>
      <v-row v-else>
        <v-col v-for="(mailing) in sortedFilteredMailings" :key="mailing.id" cols="12" sm="6" md="4" lg="3">
          <v-card class="mailing-card" @click="goToMailing(mailings.indexOf(mailing))">
            <v-card-text>
              <div class="mailing-header">
                <h2 class="title">{{ truncateText(mailing.title, 40) }}</h2>
                <span class="scheduled-time">{{ formatDateTime(mailing.scheduledtime) }}</span>
              </div>
              <p>{{ truncateText(mailing.messagetext, 100) }}</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
    <v-dialog v-model="dialog" persistent max-width="500">
      <v-card>
        <v-card-title>Выберите файл</v-card-title>
        <v-card-text>
          <v-file-input v-model="selectedFile" accept=".csv,.xlsx,.xls" label="Выберите файл" outlined hide-details
            :multiple="false"></v-file-input>
        </v-card-text>
        <v-card-actions>
          <v-btn color="light-green darken-3" :disabled="!selectedFile" @click="uploadFile">Загрузить</v-btn>
          <v-btn color="primary" @click="onCloseDialog">{{ !uploadingSuccess ? 'Отмена' : 'Закрыть' }}</v-btn>
          <v-card-text v-if="uploadingSuccess">Файл успешно загружен</v-card-text>
          <v-card-text v-if="errorMessage.length > 0">Ошибка: {{ errorMessage }}</v-card-text>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { useMailingStore } from '../components/store/mailingStore.js';
import { useAuthStore } from "../components/store/userAuth.js";

export default {
  data() {
    return {
      mailingsStore: useMailingStore(),
      loading: false, // Состояние загрузки данных
      searchQuery: '', // Добавляем переменную для хранения поискового запроса
      dialog: false,
      selectedFile: null,
      uploadingSuccess: false,
      errorMessage: '',
    };
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
  computed: {
    mailings() {
      return this.mailingsStore.mailings || [];
    },
    filteredMailings() {
      return this.mailings.filter(mailing => mailing.title.toLowerCase().includes(this.searchQuery.toLowerCase()));
    },
    sortedFilteredMailings() {
      // Клонируем отфильтрованный массив рассылок для избежания изменения исходного массива
      const filteredMailings = [...this.filteredMailings] || [];
      // Сортируем отфильтрованные рассылки по убыванию даты, чтобы новые рассылки были в начале
      filteredMailings.sort((a, b) => new Date(b.scheduledtime) - new Date(a.scheduledtime));
      return filteredMailings;
    }
  },
  methods: {
    formatDateTime(dateTimeStr) {
      const dateTime = new Date(dateTimeStr);
      return dateTime.toLocaleString();
    },
    goToMailing(mailingId) {
      this.$router.push({ name: 'MailingManage', params: { mailingId } });
    },
    createMailing() {
      // Обработчик создания рассылки
      this.$router.push({ name: 'MailingManage', params: { mailingId: -1 } });
    },
    truncateText(text, maxLength) {
      if (text.length > maxLength) {
        return text.slice(0, maxLength) + '...';
      } else {
        return text;
      }
    },
    openFileDialog() {
      this.uploadingSuccess = false;
      this.dialog = true;
    },
    async uploadFile() {
      const authStore = useAuthStore();
      const formData = new FormData();
      formData.append('file', this.selectedFile[0]);
      try {
        const response = await this.mailingsStore.uploadFileMailing(formData, authStore.user.user_data.id)
        if (!response) {
          this.selectedFile = null;
          this.mailingsStore.fetchMailingsByUserId(authStore.user.user_data.id);
          this.uploadingSuccess = true;
        } else {
          this.errorMessage = response.response.data.detail;
          this.uploadingSuccess = false;
        }
      } catch (error) {
        console.error('Ошибка загрузки рассылок:', error);
        this.uploadingSuccess = false;
      }
    },
    onCloseDialog() {
      this.dialog = false, this.selectedFile = null, this.errorMessage = '';
      if (this.uploadingSuccess) {
        // Выполните перезагрузку страницы
        window.location.reload();
      }
    }
  }
};
</script>


<style scoped>
.mailing-card {
  cursor: pointer;
  transition: transform 0.3s ease;
  margin-bottom: 20px;
  border: 2px solid #3f51b5;
  /* Цвет рамки */
  border-radius: 10px;
  /* Закругление углов */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  /* Тень */
}

.mailing-card:hover {
  transform: scale(1.05);
}

.mailing-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: bold;
}

.mailing-header .scheduled-time {
  font-style: italic;
  color: #888;
  /* серый цвет */
}

.btn-style {
  font-weight: 600;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
}
</style>
