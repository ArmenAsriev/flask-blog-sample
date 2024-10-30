# Flask Sample Web Project

This project is a sample website built with Flask, featuring user authentication, post creation, and user management. 
It demonstrates key web development concepts, such as routing, database interaction, session handling, and template rendering.

## Project Features

- **User Authentication and Registration**: Users can register, log in, log out, and access protected routes.
- **Post Creation and Display**: Users can add new posts, which are saved to the database and displayed on the homepage.
- **Session and Flash Messages**: Supports session storage for user login status and displays notifications about action outcomes, like successful registration or login errors.
- **Error Handling**: Custom 404 page for non-existent routes.
- **Modular Code Structure**: Organized into multiple files for easier management.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ArmenAsriev/flask-blog-sample.git
    cd flask-blog-sample
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create the database:
    ```bash
    python app.py
    ```

## Running the Application

Start the Flask development server:
```bash
python app.py
```



# Flask Sample Web Project

Этот проект является примером веб-сайта на Flask с функционалом авторизации, добавления статей и управления пользователями. 
Он демонстрирует основные концепции разработки веб-приложений, такие как маршрутизация, работа с базой данных, использование сессий и отображение шаблонов.

## Особенности проекта

- **Авторизация и регистрация пользователей**: Пользователи могут регистрироваться, входить и выходить из системы, а также использовать защищенные маршруты.
- **Создание и отображение записей**: Пользователи могут добавлять новые записи, которые сохраняются в базе данных и отображаются на главной странице.
- **Использование сессий и flash-сообщений**: Поддержка сессий для хранения данных о входе пользователя и отображение уведомлений о статусе действий, таких как успешная регистрация или ошибка авторизации.
- **Обработка ошибок**: Отображение страницы 404 для несуществующих маршрутов.
- **Модульная структура кода**: Разделение кода на файлы для более удобного управления.

## Установка

1. Склонируйте репозиторий:
    ```bash
    git clone https://github.com/ArmenAsriev/flask-blog-sample.git 
    cd flask-blog-sample
    ```

2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

3. Создайте базу данных:
    ```bash
    python app.py
    ```

## Запуск

Запустите сервер разработки Flask:
```bash
python app.py
