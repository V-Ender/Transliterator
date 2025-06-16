from core import load_rules, transliterate, transliterate_with_corpus, load_corpus
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import csv
import os


class TransliteratorApp:
    """
    Графическое приложение для транслитерации текста по словарю.

    Пользователь может:
    - Загрузить файл со словарем транслитерации (rules.txt).
    - Ввести текст для транслитерации.
    - Загрузить корпус (текстовый файл), если правила допускают несколько вариантов замены.
    - Получить результат транслитерации с подсветкой неоднозначных символов.

    Атрибуты:
        root (tk.Tk): Корневое окно tkinter.
        rules (dict): Словарь правил транслитерации.
        corpus_words (set): Набор слов из корпуса для контекстной замены.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Транслитератор")

        self.rules = {}
        self.corpus_words = set()

        # Кнопка загрузки словаря
        self.load_button = tk.Button(root, text="Загрузить словарь", command=self.load_rules_from_file)
        self.load_button.pack(pady=5)

        # Кнопка загрузки корпуса
        self.corpus_button = tk.Button(root, text="Загрузить корпус", command=self.load_corpus_from_file)
        self.corpus_button.pack(pady=5)

        # Поле ввода текста
        self.input_label = tk.Label(root, text="Введите текст:")
        self.input_label.pack()
        self.input_text = tk.Text(root, height=6, width=60)
        self.input_text.pack()

        # Кнопка запуска транслитерации
        self.transliterate_button = tk.Button(root, text="Транслитерировать", command=self.apply_transliteration)
        self.transliterate_button.pack(pady=5)

        # Поле вывода результата
        self.output_label = tk.Label(root, text="Результат:")
        self.output_label.pack()
        self.output_text = tk.Text(root, height=6, width=60, bg="#f0f0f0", fg="black")
        self.output_text.pack()

    def load_rules_from_file(self):
        """
        Загружает правила транслитерации из файла (.txt).

        Вызывает диалог выбора файла, парсит содержимое и сохраняет правила
        в self.rules. Показывает сообщение об успешной загрузке.
        """
        filepath = filedialog.askopenfilename(filetypes=[
            ("Text files", "*.txt"),
            ("JSON files", "*.json"),
            ("CSV files", "*.csv")
        ])
        if filepath:
            self.rules = load_rules(filepath)
            print(self.rules)
            messagebox.showinfo("Успех", f"Загружено правил: {len(self.rules)}")


    def load_corpus_from_file(self):
        """
        Загружает корпус (набор слов) из файла (.txt).

        Используется для определения наиболее вероятной транслитерации,
        если у символа есть несколько вариантов замены. Слова сохраняются в self.corpus_words.
        """
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            self.corpus_words = load_corpus(filepath)
            print(self.corpus_words)
            messagebox.showinfo("Успех", f"Загружено слов в корпусе: {len(self.corpus_words)}")

    def apply_transliteration(self):
        """
        Выполняет транслитерацию введённого текста на основе загруженных правил и корпуса.

        Если корпус загружен — используется контекстная транслитерация.
        Иначе — выбираются первый вариант при неоднозначности.
        Результат отображается в окне вывода с цветовой подсветкой неоднозначных мест.
        """
        if not self.rules:
            messagebox.showwarning("Нет правил", "Сначала загрузите файл с правилами.")
            return

        text = self.input_text.get("1.0", tk.END).strip()

        if self.corpus_words:
            chunks = transliterate_with_corpus(text, self.rules, self.corpus_words)
        else:
            chunks = transliterate(text, self.rules)  # обычная функция без корпуса

        self.output_text.delete("1.0", tk.END)

        self.output_text.tag_config("ambiguous", foreground="red", underline=True)

        for chunk, is_ambiguous in chunks:
            if is_ambiguous:
                self.output_text.insert(tk.END, chunk, "ambiguous")
            else:
                self.output_text.insert(tk.END, chunk)

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = TransliteratorApp(root)
    root.mainloop()