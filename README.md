**REST API for couriers**
----
REST API сервис, который позволит нанимать курьеров на работу,
принимать заказы и оптимально распределять заказы между курьерами, попутно считая их рейтинг и заработок.

## Запуск приложения
Для запуска нужен установленный [docker-compose](https://docs.docker.com/compose/install/)
```
$ docker-compose --env-file ./app/.env up --build -d
```
Приложение запустится на *0.0.0.0:8080*
## Запуск тестов
Для запуска тестов нужен [pytest](https://pypi.org/project/pytest/) и корректная таймзона. По умолчанию контейнер с приложением использует Europe/Moscow, такую же зону необходимо выставить на машине, с которой запускаются тесты.
Таймзону контейнера приложения можно изменить в app/Dockerfile 
```
$ pytest-3 -v
```
* **URL**

  */couriers*
  */couriers/$couriers_id*
  */orders*
  */orders/assign*
  */orders/complete*


* **Методы:**
  `GET` | `POST` | `PATCH`
