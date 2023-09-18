### Сервис для мультилейбл-классификации спутниковых снимков

1. Ссылка на сервис: [service](http://91.206.15.25:2099)

2. Описание API:

* Доступные лейблы:
```
GET: /planet/labels

Parametrs: No parameters

Example value: 
{
  "labels": [
    "string"
  ]
}
```

* Классификация спутникового снимка - лейблы:
```
POST: /planet/predict

Parametrs: Request body: multipart/form-data (.jpeg, .jpg, .png)

Example value: 
{
  "is_image_valid": true,
  "labels": [
    "string"
  ]
}
```

* Классификация спутникового снимка - вероятности принадлежности к лейблу:
```
POST: /planet/predict_proba

Parametrs: Request body: multipart/form-data (.jpeg, .jpg, .png)

Example value: 
{
  "is_image_valid": true,
  "probas": {
    "additionalProp1": 0,
    "additionalProp2": 0,
    "additionalProp3": 0
  }
}
```

___Более подробное описание API в [swagger](http://91.206.15.25:2099/docs)___

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