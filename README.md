### Сервис для мультилейбл-классификации спутниковых снимков

1. Ссылка на сервис: [service](http://91.206.15.25:2099)

2. Описание API: [swagger](http://91.206.15.25:2099/docs)

3. Запуск сервиса локально:
```
make start
```

4. Запуск сервиса локально в Docker:
```
export DOCKER_IMAGE=DOCKER_IMAGE # Поменять на название образа
make build
make run
```

5. Docker образ:
Docker образ сервиса хранится в GitLab Container Registry: 
```
export CI_REGISTRY=registry.deepschool.ru/cvr-aug23/k.khvoshchev/hw-01-service
export DOCKER_IMAGE=registry.deepschool.ru/cvr-aug23/k.khvoshchev/hw-01-service

export CI_REGISTRY_USER=USER         # Поменять на название юзера в GitLab
export CI_REGISTRY_PASSWORD=PASSWORD # Поменять на пароль юзера в GitLab

make login
make pull
```

6. Запуск тестов:
```
make tests_unit        # Для запуска юнит-тестов
make tests_integration # Для запуска интеграционных тестов
make tests             # Для запуска всех тестов
```

7. Запуск линтера:
```
make lint
```

8. GitLab CI Pipeline:

* Сборка docker-образа
* Линтеры
* Юнит тесты
* Интеграционные тесты
* Запуск сервиса
* Остановка сервиса