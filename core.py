import re
import random

def load_rules(filename):
    """
    Загружает словарь транслитерации в переменную rules
    Пример файла rules.txt
    ая=aja
    р=r
    п=p
    а=a
    н=N,n
    :param filename: str, путь к файлу
    :return: dict, словарь транслитераций
    """
    rules = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                rules[key] = value.split(',') if ',' in value else value
    return rules


def save_rules(rules, filename):
    """
    Сохраняет словарь транслитераций rules в файл, путь до которого filename
    :param rules: dict, словарь транслитераций
    :param filename: str, путь до файла
    :return:
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for key, value in rules.items():
            f.write(f"{key}={value}\n")


def transliterate(text, rules):
    """
    Транслитерирует текст по словарю rules
    :param text: str, текст для транслитерации
    :param rules: dict, словарь
    :return: массив, где элементами являются кортежи (траслитерированный токен, True/False)
             второй элемент кортежа показывает, является транслитерация единстенной
    """
    sorted_rules = sorted(rules.items(), key=lambda x: -len(x[0]))
    result_chunks = []
    i = 0
    while i < len(text):
        matched = False
        for key, val in sorted_rules:
            if text[i:i+len(key)] == key:
                matched = True
                if isinstance(val, list):
                    chosen = val[0]
                    result_chunks.append((chosen, True))
                else:
                    result_chunks.append((val, False))
                i += len(key)
                break
        if not matched:
            result_chunks.append((text[i], False))
            i += 1
    return result_chunks


def load_corpus(filepath):
    """
    Загружает корпус из файла
    :param filepath: str, путь до файла
    :return: set, множество слов из корпуса
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read().lower()
            return set(re.findall(r'\b\w+\b', text))
    except Exception as e:
        raise Exception("Ошибка загрузки корпуса")


def transliterate_with_corpus(text, rules, corpus):
    """
    Транслитерирует текст по словарю rules и корпусу corpus
    :param text: str, текст
    :param rules: dict, словарь траснлитераций
    :param corpus: set, множество слов из корпуса
    :return: массив, где элементами являются кортежи (траслитерированный токен, True/False)
             второй элемент кортежа показывает, является транслитерация единстенной
    """
    sorted_rules = sorted(rules.items(), key=lambda x: -len(x[0]))
    result_chunks = []  # список кортежей (строка, is_ambiguous)
    i = 0
    while i < len(text):
        matched = False
        for key, val in sorted_rules:
            if text[i:i+len(key)] == key:
                matched = True
                i_end = i + len(key)

                if isinstance(val, list):
                    word_start = i
                    while word_start > 0 and text[word_start - 1].isalpha():
                        word_start -= 1
                    word_end = i_end
                    while word_end < len(text) and text[word_end].isalpha():
                        word_end += 1
                    source_word = text[word_start:word_end]

                    best_variant = None
                    for variant in val:
                        replaced_text = (
                            source_word[:i - word_start] +
                            variant +
                            source_word[i_end - word_start:]
                        )

                        transliterated = ""
                        j = 0
                        while j < len(replaced_text):
                            submatched = False
                            for sub_key, sub_val in sorted_rules:
                                if replaced_text[j:j+len(sub_key)] == sub_key:
                                    transliterated += (
                                        sub_val[0] if isinstance(sub_val, list) else sub_val
                                    )
                                    j += len(sub_key)
                                    submatched = True
                                    break
                            if not submatched:
                                transliterated += replaced_text[j]
                                j += 1

                        if transliterated in corpus:
                            best_variant = variant
                            break

                    if best_variant:
                        result_chunks.append((best_variant, False))
                    else:
                        fallback = val[0]
                        result_chunks.append((fallback, True))
                else:
                    result_chunks.append((val, False))
                i = i_end
                break

        if not matched:
            result_chunks.append((text[i], False))
            i += 1

    return result_chunks

