# Система управления рассылками

Это приложение предназначено для управления рассылками через различные каналы связи, такие как электронная почта, сервисы Notisend и Sendsay (доступ ограничен), а также Telegram.

## Описание

Система управления рассылками позволяет пользователям создавать, редактировать и удалять рассылки, а также отправлять их через различные каналы связи. Пользователи могут загружать списки рассылок из различных источников, таких как Excel, CSV файлы (в папке filesToUpload приведены примеры файлов для загрузки), а также через REST API в формате JSON. Рассылки могут быть запущены как в ручном режиме, так и по API.

## Требования

- Python 3.x
- Vue.js
- PostgreSQL
- FastAPI

## Запуск с использованием Docker Compose

1. Убедитесь, что у вас установлен Docker и Docker Compose.

2. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/KosmixGT/mailforge.git
    ```

3. Перейдите в каталог проекта:

    ```bash
    cd repository
    ```

4. Отредактируйте файл `docker-compose.yml` для настройки подключения к удаленной базе данных и других параметров. Для этого отредактируйте соответствующие параметры в файле `docker-compose.yml`. Например:

    ```yaml
    services:
      backend:
        environment:
        - DATABASE_URL=url
    ```

5. Запустите контейнеры с помощью Docker Compose:

    ```bash
    docker-compose up -d
    ```

   Это запустит все сервисы, описанные в файле `docker-compose.yml`, в фоновом режиме.

6. После запуска контейнеров вы можете открыть ваше приложение в браузере по адресу [http://localhost:your_port](http://localhost:your_port), где `your_port` - порт, указанный в вашем файле `docker-compose.yml`.

7. При необходимости вы можете настроить другие параметры окружения, такие как время действия токена авторизации, алгоритм шифрования и URL для `VUE_APP_BACKEND_URL`, также в файле `docker-compose.yml` в секции `environment`.

8. По умолчанию, файл `docker-compose.yml` уже содержит все необходимые параметры для работы. База данных реализована на хостинге CleverCloud, строка подключения к ней уже прописана.


## Установка

1. Клонируйте репозиторий: `git clone https://github.com/yourusername/yourproject.git`
2. Перейдите в папку проекта: `cd yourproject`
3. Установите зависимости для бэкенда: `pip install -r requirements.txt`
4. Установите зависимости для фронтенда: `npm install`
5. Создайте базу данных PostgreSQL и настройте подключение в файле `.env`, создав его в корне проекта.
6. Запустите сервер: `uvicorn main:app --reload`
7. Запустите фронтенд: `npm run serve`
8. Откройте приложение в браузере: `http://localhost:8080`

## Использование

1. Зарегистрируйтесь в системе или войдите под своим аккаунтом.
2. Создайте новую рассылку, выбрав нужные параметры и каналы связи или загрузите их из файла.
3. Добавьте получателей из уже существующих (ранее уже получавшие рассылки) или добавьте новых.
4. Отправьте рассылку.
5. Просматривайте и управляйте списком рассылок.
