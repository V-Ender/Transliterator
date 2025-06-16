import unittest
from core import transliterate, transliterate_with_corpus

class TestTransliteration(unittest.TestCase):

    def test_basic_transliteration(self):
        rules = {
            "п": "p",
            "а": "a",
            "р": "r",
            "к": "k"
        }
        text = "парк"
        expected = "park"
        result = transliterate(text, rules)

        # Преобразуем результат в строку, если это список кортежей
        if isinstance(result, list):
            result = ''.join(chunk for chunk, _ in result)

        self.assertEqual(result, expected)

    def test_multi_variant_random_transliteration(self):
        import random
        random.seed(0)  # фиксируем для предсказуемости

        rules = {
            "н": ["n", "ŋ"],
            "о": "o"
        }
        text = "но"
        result = transliterate(text, rules)

        # если результат — список кортежей, собираем строку
        if isinstance(result, list):
            result = ''.join(chunk for chunk, _ in result)

        self.assertEqual(result, "no")

    def test_transliteration_with_corpus(self):
        rules = {
            "н": ["n", "ŋ"],
            "о": "o",
            "д": "d"
        }
        text = "нод"
        corpus_words = {"nod"}
        result_chunks = transliterate_with_corpus(text, rules, corpus_words)
        joined_result = ''.join(chunk for chunk, _ in result_chunks)
        self.assertEqual(joined_result, "nod")

    def test_transliteration_with_corpus_2(self):
        rules = {
            "н": ["n", "ŋ"],
            "о": "o"
        }
        text = "но"
        corpus_words = {"ŋo"}  # только одна из форм есть
        result_chunks = transliterate_with_corpus(text, rules, corpus_words)
        joined_result = ''.join(chunk for chunk, _ in result_chunks)
        self.assertEqual(joined_result, "ŋo")

    def test_transliteration_with_corpus_uncertain(self):
        rules = {
            "н": ["n", "ŋ"],
            "о": "o"
        }
        text = "но"
        corpus_words = {"somethingelse"}  # ни один не подходит
        result_chunks = transliterate_with_corpus(text, rules, corpus_words)
        options = {"no", "ŋo"}
        joined_result = ''.join(chunk for chunk, _ in result_chunks)
        self.assertTrue(any(joined_result == o for o in options))
        # Проверка, что флаг "неуверенности" включен
        self.assertTrue(any(is_uncertain for _, is_uncertain in result_chunks))

if __name__ == "__main__":
    unittest.main()