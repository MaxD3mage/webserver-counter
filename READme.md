# Webserver счетчик посещений
Это простой Webserver (Задание с [Anytask](https://anytask.org/course/1030)), 
который умеет считать статистику посещений, а так же уникальных посетителей.
# Описание использование
 * Запустит сервер и зайти на сайт ```http://localhost:8080/```
 * Можно посмотреть статистику посещений добавив ```/stats/{period}```, где вместо period подставляем day/month/year/total
   Например ```http://localhost:8080/stats/day```
 * Можно посмотреть статистику уникальных посещений добавив ```/stats/{period}```, 
   где вместо period подставляем day/month/year/total
   Например ```http://localhost:8080/stats/day```
# Декомпозиция
 Сердцем является ```webserver.py```, а visits.db база данных которая хранит посещения (sql)

Made by **MaxDamage**