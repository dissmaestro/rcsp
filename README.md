# fastapi-todo-lr1

```bash
# установка с прокси и без
pip install --user --proxy http://login:pass@192.168.232.1:3128 -r requirements.txt
pip install --user -r requirements.txt

cd app
uvicorn main:app --reload
```

С docker
```bash
sudo docker build -t 2020-3-00-lr1 .
sudo docker run --rm -p 8000:8000 2020-3-00-lr1

# with database save
sudo docker run --rm -p 8000:8000 -v "${PWD}/data/":/code/data/ 2020-3-00-lr1

# development
sudo docker run --rm -p 8000:8000 -v "${PWD}/app":/code/app -v "${PWD}/data/":/code/data/ 2020-3-00-lr1

# generate
sudo docker build -t 2020-3-00-lr1-generate -f Dockerfile_generate .
sudo docker run --rm --network=host 2020-3-00-lr1-generate
```

Задачи на ЛР1

0. Склонировать к себе этот проект. Загрузить в личный проект по указанию преподавателя. Дополнить gitignore. Разработку вести через создание задач, веток и merge request.
1. Сделать Docker-образ, в ридми прописать режим работы пользователя (построил-запустил) и разработчика (запустил автообновляемый контейнер).
2. Подготовить postman:
    * создать коллекцию
    * через переменные окружения настроить URL
    * реализовать все запросы
    * экспортировать запросы и сохранить в своём проекте
3. Починить баги:
    * Падение при создании пустой задачи. Реализовать с помощью status\_code
    * Падение при удалении несуществующей задачи
    * Добавить ограничение на длину загружаемой записи в 500 символов
    * Есть ли ещё?
4. Доработать:
    * Отрефакторить модель, заменив task на title - заголовок задачи
    * Задачу дополнить полем details (подробное описание задачи) с произвольным текстом. На подробном представлении добавить второй textarea для details
    * На главную страницу добавить кнопку "выполнено" для невыполненных задач и "не выполнено" для выполненных. По нажатию менять статут тудушки
    * Добавить постраничный просмотр, если тудушек больше 10
    * Добавить скрипт генерации 20 тудушек со случайными заголовками. Добавить в ридми порядок запуска этого скрипта через Docker
    * Добавить в модель тег для задачи, реализовать как enum со значениями учёба/личное/планы. Добавить на страницу редактирования тудушки выпадающий список тегов
