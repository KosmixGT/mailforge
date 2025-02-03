# Этап сборки
FROM node:16-alpine as build-stage

# Установка глобальных зависимостей
RUN npm install -g @vue/cli@5.0.8

# Установка рабочей директории
WORKDIR /app

# Копирование package.json и package-lock.json
COPY package*.json ./

# Установка зависимостей
RUN npm install

# Копирование остальных файлов проекта
COPY . .

# Сборка проекта
RUN npm run build

# Финальный этап
FROM nginx:alpine as production-stage

# Копирование собранных файлов из этапа сборки
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Копирование конфигурации Nginx (если требуется)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Открытие порта
EXPOSE 80

# Запуск Nginx
CMD ["nginx", "-g", "daemon off;"]