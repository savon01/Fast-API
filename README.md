## Требования

- Docker
- Docker Compose

## Установка

## Откройте выбранную вами среду разработки и склонируйте репозиторий проекта:

### git clone https://github.com/savon01/Fast-API

## В корневой директории создайте файл .env и создайте следущие перменные:
### YOUR_DB = "your_postgres_db_name"
### YOUR_USER = "your_postgres_username"
### YOUR_PASSWORD = "your_postgres_password"
### YOUR_HOST = "your_postgres_host"
### YOUR_PORT = "your_postgres_port"


### POSTGRES_DB = "your_postgres_db_name"
### POSTGRES_USER = "your_postgres_username"
### POSTGRES_PASSWORD = "your_postgres_password"


## Собрать и запустить контейнеры:
### docker-compose up -d --build

## Запустить контейнер с приложением:
### docker-compose up -d web 

## Запустить контенер с тестами:
### docker-compose run tests 


## Задание номер 3 расположено в файле three.py


