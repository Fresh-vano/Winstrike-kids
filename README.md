
<p align="center">
    <img src="./logo.png" alt="Логотип проекта" width="150" style="display: inline-block; vertical-align: middle; margin-right: 10px;"/>  <br/>
     <H2 align="center">Команда Winstrike</H2> 
    <H2 align="center">Кейс ФГБУ "НМИЦ ТПМ" Минздрава Россиии</H2> 
</p>

> Команда Winstrike представляет новаторский программный модуль для распознавания текста с этикеток детского питания по фотографии, разработанный на основе технологий искусственного интеллекта. Данный программный продукт является мощным инструментом для автоматизации анализа, который способствует предотвращению использования продуктов, которые могут быть неоптимальными или вредными для здоровья ребёнка.


## Установка и запуск

**Наше решение разделено на две ключевые части. Первая часть включает в себя подробное руководство по развёртыванию без необходимости взаимодействия с интерфейсом, что обеспечивает быстрое и эффективное тестирование. Вторая часть предоставляет подробные инструкции по развертыванию решения с использованием интерфейса, обеспечивая при этом максимальную удобство и интуитивную навигацию.**

***Часть 1:***
----------

*1. Загрузите папку "1 часть" и откройте её в вашей предпочитаемой среде разработки (IDE).* 

*2. Откройте терминал в IDE и введите туда следующую команду:* 

```python
python -m venv .venv
```
*3. Дождитесь создание папки `.venv` затем введите следующую команду:*

```python
.\.venv\Scripts\activate
```
*4. После активации установите все библиотеки (весрия python==3.10+) при помощи данной команды:*

```python
pip install -r requirements.txt
```
*5. Дождитесь установки всех библиотек.*

*6. Запустите скрипт поиска информации введя команду, изменив путь до изображения `test.jpg` из примера на свой ```Внимание!!!``` путь должен быть обсолютным, помещен в двойные ковычки, должны быть двойные \\\\ .*

```python
python.exe .\searching_alogrithm.py "C:\hack\\test.jpg"
```
*7. После выполнения скрипта в концоли отобразится путь до сохраненного `json` файл со всей необходимой информацией*

*Пример `json` файла*

```json
{"name": "Сухие каши и крахмалистые продукты", // Наименование продукта
"manufacturer": "N/A", // Фирма-производитель
"category_id": 1, // ID-категории продукта
"description": " мясо кролика, вода, мука рисовая, масло растительное продукт может содержать незначительное количество", // Cостав
"characteristics": {"energy_value": "420",  // Энергетическая ценность
                    "sodium": "N/A",		// Содержание натрия
                    "total_sugar": "N/A",	// Содержание сахарозы
                    "free_sugar": "N/A",	// Содержание свободных сахаров
                    "total_protein": "7",	// Содержание белка
                    "total_fat": "5,5",     // Содержание жиры
                    "fruit_content": "N/A",	// Наличие фруктов
                    "age_marking": "N/A",	// Возрастные ограничения
                    "high_sugar_front_packaging": "Нет", // Высокое содержание сахара
                    "labeling": "Соответствует"}} // Присутствие обязательной маркировки

```
***Часть 2:***
----------

### Backend
Для запуска API и алгоритма обработки изображения нейросетью требуется:

*1. Установить требуемые библиотеки.*

```python
pip install -r requirements.txt
```

*2. Установить PostgreSQL с оффициального сайта.*

*3. Указать данные для подключения к базе данных в файле `config.py`*

*4. Запустить проект. Запуск производится запуском файла `main.py`* 

*5. Произвести миграцию базы данных. При помощи следующей команды*

```python
flask db upgrade
```
При загрузке изображения на сервер посредством API, оно сохраняется в папку `static/`.

### Frontend
Для запуска приложения требуется:

*1. Установить требуемые библиотеки.*

```cmd
npm install
```

или

```cmd
yarn install
```

*2. Запустить проект.* 

```cmd
npm run start
```
*3. Путь до API сервера указывается в файле `frontend/src/confog.js` .*

### Docker
Для запуска данного проекта в среде Docker требуется:

*1. Установить Docker Desktop с оффициального сайта.*

*2.1. Для запуска всего приложения в папке `Winstrike-kids/'Часть 2'/` требуется выполнить следующую команду:*

```cmd
docker-compose up
```

После установки всех библиотек и зависимостей будет созданно 3 docker контейнера:
- _frontend_ - с сайтом проекта на порту 3000
- _backend_ - с API и нейросетью проекта на порту 5000
- _db_ - база данных PostgreSQL для сохранения результатов анализа на порту 5432

# Пример использования, иллюстрированный процессом обработки скринкаста.




https://github.com/Fresh-vano/Winstrike-kids/assets/74467916/bc57ae3c-4c43-493f-bae4-74a649f2868a




*Ознакомиться с видео в хорошем качестве можете перейдя по [ссылке](https://drive.google.com/file/d/1-_Ky1P6hfJHz-jfd6TEr2ljGDHaUzHa2/view) или открыть указаную нами ссылку на сайте цифрового прорыва.*

# Пример работы програмного модуля

![gif](https://github.com/Fresh-vano/Winstrike-kids/assets/74467916/36c37fdb-3bc5-4a41-b9c7-9a5d97ddbf63)




Все права защищены. &copy; Winstrike.
