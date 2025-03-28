# Система управления рассылками

Это приложение предназначено для управления рассылками через различные каналы связи, такие как электронная почта, сервисы Notisend и Sendsay (доступ ограничен), а также Telegram.

## Описание

Система управления рассылками позволяет пользователям создавать, редактировать и удалять рассылки, а также отправлять их через различные каналы связи. Пользователи могут загружать списки рассылок из различных источников, таких как Excel, CSV файлы (в папке filesToUpload приведены примеры файлов для загрузки), а также через REST API в формате JSON. Рассылки могут быть запущены как в ручном режиме, так и по API.

## Архитектура микросервисов
### Основные компоненты:
1.	**API Gateway (FastAPI)** — обрабатывает запросы от клиентов и маршрутизирует их к соответствующим микросервисам.
2.	**Mailing Service** — отвечает за создание, редактирование и управление рассылками.
3.	**Delivery Service** — обрабатывает и отправляет сообщения через различные каналы связи.
4.	**History Service** — хранит историю отправленных сообщений и их статусы.
5.	**Auth Service** — аутентификация и управление пользователями.
6.	**Message Broker (RabbitMQ)** — обеспечивает асинхронное взаимодействие между сервисами.
7.	**PostgreSQL** — основная база данных для хранения информации о рассылках и пользователях. (реализовано на CleverCloud, удалённо)
8.	**Frontend (Vue.js)** — пользовательский интерфейс системы.


## Первоначальные требования

* Возможность создавать, редактировать, удалять и запускать рассылки.
* Поддержка различных каналов связи (email, Telegram, сторонние API).
* Управление списками получателей, возможность загружать их из внешних источников.
* Запланированные и повторяющиеся рассылки.
* Отслеживание статуса отправленных сообщений (доставлено, ошибка, отказ).
* Аутентификация и разграничение прав пользователей (администраторы, менеджеры).
* Интеграция с внешними сервисами (SMTP, Telegram API, Sendsay и др.).

## Инструментарий для реализации

### 1. Языки программирования и фреймворки
* Backend: Python (FastAPI)
* Frontend: Vue.js (с использованием Vuetify и Pinia)
### 2. Среда разработки (IDE)
    Visual Studio Code (VS Code)  
### 3. База данных
    PostgreSQL  
### 4. Инфраструктура и контейнеризация
* Docker (для контейнеризации и развертывания приложения)
* Git (для управления версиями кода)
* RabbitMQ (для обмена сообщениями между микросервисами)
### 5. Основные зависимости (Python)

В проекте используются следующие ключевые библиотеки:

* FastAPI — асинхронный веб-фреймворк для разработки API
* SQLAlchemy — ORM для работы с базой данных
* psycopg2 — драйвер для работы с PostgreSQL
* Pydantic — валидация данных
* Uvicorn — ASGI-сервер для запуска FastAPI
* aiofiles, aiosignal, aiohttp — асинхронные инструменты для работы с файлами и HTTP-запросами
* python-dotenv — работа с переменными окружения
* bcrypt, passlib — хеширование паролей
* requests — выполнение HTTP-запросов
### 6. Основные зависимости (Frontend)
* Vue.js — фреймворк для разработки пользовательского интерфейса
* Vuetify — UI-библиотека на основе Material Design
* Pinia — управление состоянием приложения
### 7. Управление зависимостями
* Backend: pip + requirements.txt
* Frontend: npm
### 8. Хостинг и развертывание
Исходный код загружен в репозиторий (GitHub) и упакован в контейнер Docker для удобного развертывания.

## Архитектурные паттерны и практики

### Общая архитектура
#### Clean Architecture
Проект построен на принципах чистой архитектуры с явным разделением на слои:
- API слой (app/api)
- Application слой (app/application) 
- Domain слой (app/domain)
- Infrastructure слой (app/infrastructure)

Каждый внутренний слой не зависит от внешних слоев, что обеспечивает гибкость и тестируемость.

### Application слой
#### DTO Pattern (app/application/dto)
Используется для безопасной передачи данных между слоями. DTO объекты:
- Скрывают внутреннюю структуру доменных объектов
- Оптимизируют передачу данных
- Предоставляют контракт для API

#### Service Layer (app/application/services) 
Содержит бизнес-логику приложения:
- Оркестрирует работу с репозиториями
- Преобразует данные между DTO и доменными моделями
- Реализует конкретные сценарии использования

### Domain слой
#### Domain Models (app/domain/models)
Описывают бизнес-сущности и правила:
- Независимы от инфраструктуры
- Содержат только бизнес-логику
- Являются ядром приложения

#### Repository Interfaces (app/domain/interfaces)
Определяют контракты для работы с данными:
- Абстрагируют способ хранения
- Позволяют менять реализацию хранилища
- Упрощают тестирование

### Infrastructure слой
#### Repository Pattern (app/infrastructure/repositories)
Реализует доступ к данным:
- Изолирует работу с базой данных
- Предоставляет единый интерфейс для доступа к данным
- Поддерживает разные типы хранилищ

#### Database Models (app/infrastructure/database/models)
Описывают структуру хранения в БД:
- Отражают схему базы данных
- Содержат ORM-маппинги
- Независимы от бизнес-логики

#### Unit of Work (app/infrastructure/database)
- Управление транзакциями
- Атомарные операции

#### Adapter Pattern (app/infrastructure/repositories)
- Адаптация внешних интерфейсов
- Конвертация данных

### Порождающие паттерны
#### Factory Method (app/application/services)
- Создание объектов
- Изоляция логики создания

### Общие практики
- Dependency Injection
- Async Programming
- Type Hints
- SOLID принципы

## Запуск с использованием Docker Compose

1. Убедитесь, что у вас установлен Docker и Docker Compose.

2. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/KosmixGT/mailforge.git
    ```

3. Перейдите в каталог проекта:

    ```bash
    cd mailforge
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


## Альтернативный запуск (локально без Docker)

1. Клонируйте репозиторий: `git clone https://github.com/yourusername/yourproject.git`
2. Перейдите в папку проекта: `cd mailforge`
3. Установите зависимости для бэкенда для каждого сервиса: `pip install -r requirements.txt`
4. Установите зависимости для фронтенда: `npm install`
5. Создайте базу данных PostgreSQL и настройте подключение в файле `.env`, создав его в корне проекта. Или воспользуйтесь url удалённой базы данных, которая уже прописана в файле `docker-compose.yml`
6. Запустите сервер: `uvicorn main:app --reload --port 800{0-9}` для каждого сервиса свой порт
7. Запустите фронтенд: `npm run serve`
8. Откройте приложение в браузере: `http://localhost:8080`

## Использование

1. Зарегистрируйтесь в системе или войдите под своим аккаунтом.
2. Создайте новую рассылку, выбрав нужные параметры и каналы связи или загрузите их из файла.
3. Добавьте получателей из уже существующих (ранее уже получавшие рассылки) или добавьте новых.
4. Отправьте рассылку.
5. Просматривайте и управляйте списком рассылок.
