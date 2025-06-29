Транслитератор с поддержкой контекстного выбора вариантов
Описание
Приложение на python, реализующее транслитерацию текста по словарю с возможностью загрузки корпуса примеров для уточнения неоднозначных вариантов.

Основные возможности:

1) Загрузка словаря транслитерации из файла.

2) Транслитерация текста по заданному словарю.

3) Поддержка множественных вариантов транслитерации для одних и тех же символов.

4) Загрузка корпуса слов-примеров для выбора правильного варианта транслитерации в контексте.

5) GUI на tkinter с удобным вводом текста, загрузкой правил и корпуса, выводом результата с подсветкой неоднозначных участков.

6) Возможность сохранения и загрузки нескольких словарей.

Структура файлов

core.py                  # Основной модуль с логикой транслитерации

gui.py                   # Интерфейс на tkinter

tests.py                 # Набор юнит-тестов функций

rules.txt                # Пример файла со словарем

corpus.txt               # Пример корпуса слов

README.md                # Этот файл

Как использовать
1) Нажмите кнопку "Загрузить правила" для выбора файла с правилами транслитерации.

2) При необходимости загрузите корпус через кнопку "Загрузить корпус".

3) Введите текст для транслитерации.

4) Нажмите "Транслитерировать" — результат появится в нижнем поле.

5) Неоднозначные места будут подсвечены цветом.
