# Лабораторный проект по теме "Формирование ленты новостей по предпочтениям (Тегам)" предмет МиМОБОД
### Магистранта группы 056241 Хлопцева Андрея Алексеевича

# Задача
Создать проект, который будет агрегировать новости с интернет-ресурсов и с помощью алгоритмов машинного обучения устанавливать их приналежность к различным темам.

# Основная идея
Необходимо создать проект, состоящий из 3 частей:

1. Расширяемый модуль в который можно дабивать обработчики открытых API интернет-ресурсов. Данный модуль необходим для сбора информации
2. Модуль, который будет рассортировывать и хранить собранную и обработанную информацию
3. Модуль, реализующий некоторые алгоритмы машинного обучения, необходимые для классификации полученной информации и функции обработки полученной информации

# Описание реализации проекта
## Получение данных

Для начала разработки был выбран один из самых популярных интернет-изданий TheGuardian. Данный ресурс был выбран по нескольким причинам
1. Очень обширная база новостей на различные темы
2. Имеется открытое API, для получения новостей (для использования надо запросить Api-key)
3. API запросы позволяют выбрать темы скачиваемых новостей, что сильно ускоряет реализацию проекта, т.к. позволяет пропустить этап ручной обработки (разметки) новостей

Чтобы начать использовать API необходимо пройти по ссылке https://open-platform.theguardian.com/access/ и запросить ключ доступа. Этим ключом мы будем помечать все наши запросы, чтобы нам была доступна не только тестовая коллекция новостей, но и остальные статьи

После получения ключа и установки соединения с сервером необходимо реализовать несколько запросов для получения статей. В данном проекте статья включает в себя:
1. Заголовок
2. Текст
3. Ссылка на статью
4. Ссылка на главную фотографию
5. Время размещения статьи

В модуле TheGuardianParser было реализовано 2 основных вида команд:
1. Получение статей по тегу (это необходимо для получения размеченного набора статей, нужных для тренировки алгоритмов машинного обучения)
2. Получение последних новостей. Данный запрос не будет содержать тега, определяющего, какие именно новости скачивать, и будет производится каждые 5 минут.

Ограничения API состоит в том, что за один запрос можно получить максимум 50 статей, поэтому для запросов было реализовано постраничное чтение для получения необходимого кол-ва данных.

## Обработка данных
Для классификации статей был использован SVM алгоритм машинного обучения. Классификация будет производится по 7 темам:
* Спорт
* Политика
* Наука
* Фильмы
* Музыка
* Экономика
* Все (включает все предыдущие темы + темы, не упомянутые в классификаторе)

Для того, чтобы лучше обучить ядро SVM алгоритма, данные необходимо очистить от лишнего "мусора" и "шума". Поэтому был разработан специальный модуль TextProcessor, который:
1.  переводит текст в нижний регистр;
2.  удаляет HTML тэгов (если они есть в тексте);
3.  заменяет URL на одно слово (“httpaddr”);
4.  заменяет email-адресов на одно слово (“emailaddr”);
5.  заменяет числа на одно слово (“number”);
6.  заменяет знаков доллара ($) на слово “доллар”;
7.  заменяет форм слов на исходное слово. Такой подход называется stemming;
8.  удаляет остальные символы и заменяет их пробелами;
9.  удаляет и заменяет "стоп-слова" (слова, не меющие никакой информации) в тексте.
10. подсчитывает топ самых популярных слов, для генерации словаря обучения

Для реализации этих операций были использованы регулярные выражения и Python библиотека nltk с английским корпусом текстов

После обработки группы статей, объединённых одной темой, на выходе мы получаем набор векторов, каждый из которых состоит только из информационных слов в их начальной форме + словарь самых популярных слов по данной теме.

После этого каждая статья кодируется в виде бинарного вектора X, длинной равно длине словаря. 0 на i-м месте означает, что i-e слово в словаре не встречалось в данной статье, 1 - наоборот

## Хранение данных
После обработки статей их необходимо сохранить для дальнейшей обработки и обучения SVM. Для этого была использована база данных MySQL, где каждому набору данных соответствует своя таблица состоящая из:
1. Id - уникальный номер каждой обработанной статьи
2. Текст - строка, содержащая текст статьи (для повторного обучения в случае необходимости)
3. X - бинарный вектор, обработки статьи на словаре этой темы
4. y - бинарный вектор, для обучения SVM состоящий из 0. Единственный элемент равен 1 - номер темы, к которой принадлежит статья

Ещё в базе данных хранится одна общая таблица для статей, которые используются непосредственно для формирования ленты новостей, она состоит из:
1. Id - уникальный номер каждой обработанной статьи
2. Заголовок - строка содержащая заголовок статьи
3. Текст - строка содержащая обрезанный текст статьи (около 100 символов)
4. Ссылка на статью - ссылка по которой можно перейти к оригиналу статьи
5. Ссылка на главную фотографию - ссылка по которой будет грузится превью статьи
6. Время размещения статьи - дата, когда данная статья была размещена
7. Тег - строка, содержит тему к которой принадлежит данная статья

Также в папку "Cache models" были сохранены словари для каждой темы и коеффициенты SVM, чтобы не было необходимости обучать их заново при каждом запуске

## Классификация статей
По итогу предыдущих пунктов созданы модули для сбора и обработки информации, необходимой для обучения алгоритмов машинного обучения, которые должны классифицировать поступившую статью по одной из 6 тем (или не классифицировать ни к одной, тогда статья будет помечена тегом all). Для этого было создано 6 ядер SVM с функцией Гауссового ядра. Для каждого ядра был подготовлен свой словарь самых популярных слов (1200 слов) в статьях данной темы, и набор обработанных статей, состоящий из 12000 векторов (по 2000 на каждую тему).

Однако, прежде чем обучать модели, необходимо было выбрать правильные коеффициенты C и sigma для тренировки модели. Для этого был создан небольшой набор данных 3000 статей (по 500 с каждой темы) в качесте тренировочного набора и 600 (по 100 с каждой темы) в качесте валидационного. После этого алгоритмом полного перебора (brute-force) были выявлены коеффициенты для каждого ядра, на котором наблюдается наименьшее число отклонений.

* Спорт: С=100, sigma=0.0209
* Политика: С=100, sigma=0.0023
* Наука: С=100, sigma=0.0082
* Фильмы: С=100, sigma=0.0167
* Музыка: С=100, sigma=0.0182
* Экономика: С=100, sigma=0.0137

Послу получения коеффициентов, ядра были обучены на выборке из 12000 статей. После этого точность обучения была проверена на новой тестовой выборке в 2400 (по 400 статей каждой темы). Полученная точность:

* Спорт: 89.83333333333333%
* Политика: 96.95833333333333%
* Наука: 99.08333333333333%
* Фильмы: 92.08333333333333%
* Музыка: 92.66666666666666%
* Экономика: 98.95833333333334%

## Визуализация ленты новостей

Для визуализации ленты новостей был создан проект на Django 3.1. Данный проект содержит 1 страницу, на которую выводятся новости в зависимости от тега, выбранного в сверху страницы. Перед запуском проекта с TheGuardian были скаченны и классифицированы 500 статей. Далее скрипт в фоновом потоке каждые 5 минут обращается к серверу за получением новых статей. После их классификации они загружаются в базу занных, и отображаются после перегрузки страницы или смены фильтра.

### Базовый интерфейс (фильтр=все) 
![Базовый интерфейс](/screenshots/all_news.png?raw=true)

### Фильтр фильмы
![Фильмы](/screenshots/films_news.png?raw=true)

### Фильтр экономика
![Экономика](/screenshots/economy_news.png?raw=true)