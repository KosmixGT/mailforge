import { defineStore } from 'pinia';
import axios from 'axios';
import authHeader from "../services/auth-header";

export const useMailingStore = defineStore('mailing', {
  state: () => ({
    mailings: [],
    currentMailing: null,
  }),

  actions: {
    async fetchMailingsByUserId(userId) {
      try {
        const savedMailings = JSON.parse(localStorage.getItem('mailings'));
        if (savedMailings) {
          this.mailings = savedMailings;
        } else {
          const response = await axios.get(`/mailings/by_user/${userId}`);
          this.mailings = response.data;
          localStorage.setItem('mailings', JSON.stringify(response.data));
        }
      } catch (error) {
        console.error('Error fetching mailings by user ID:', error);
      }
    },
    async fetchMailing(mailingId) {
      try {
        const response = await axios.get(`/mailings/${mailingId}`);
        this.currentMailing = response.data;
      } catch (error) {
        console.error('Error fetching mailing:', error);
      }
    },

    async fetchMailings() {
      try {
        const response = await axios.get('/mailings');
        this.mailings = response.data;
      } catch (error) {
        console.error('Error fetching mailings:', error);
      }
    },

    async createMailing(mailing, user_id) {
      try {
        await axios.post('/mailings/create', mailing, {headers: authHeader()});
        // Обновляем состояние после успешного создания рассылки
        const response = await axios.get(`/mailings/by_user/${user_id}`);
        // this.mailings = response.data;
        const newMailing = response.data;
        // Добавление новой рассылки к списку рассылок в хранилище
        this.mailings.push(newMailing);
        localStorage.setItem('mailings', JSON.stringify(response.data));
        window.location.reload();
      } catch (error) {
        console.error('Error creating mailing:', error);
      }
    },

    async deleteMailing(mailingId, user_id) {
      try {
        await axios.delete(`/mailings/delete/${mailingId}`)   
        //Обновляем состояние после успешного удаления рассылки
        const response = await axios.get(`/mailings/by_user/${user_id}`);
        this.mailings = response.data;
        localStorage.setItem('mailings', JSON.stringify(response.data));
        window.location.reload();
      } catch (error) {
        console.error('Error deleting mailing:', error);
      }
    },
    async updateMailing(mailingId, user_id, mailing) {
      try {
        await axios.put(`/mailings/update/${mailingId}`, mailing)
        //Обновляем состояние после успешного обновления рассылки
        const response = await axios.get(`/mailings/by_user/${user_id}`);
        this.mailings = response.data;
        localStorage.setItem('mailings', JSON.stringify(response.data));
        window.location.reload();
      } catch (error) {
        console.error('Error updating mailing:', error);
      }
    },
    //Загрузка состояния из локального хранилища при создании хранилища
    onInit() {
      const storedMailings = localStorage.getItem('mailings');
      if (storedMailings) {
        this.mailings = JSON.parse(storedMailings);
      }
    }
  }
});
