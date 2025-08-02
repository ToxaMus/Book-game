import random
import re
from itertools import count

import nltk
from nltk.tokenize import sent_tokenize


class Fragment:
    def __init__(self, text):
        """Инициализация с предварительной загрузкой ресурсов NLTK"""
        self._ensure_nltk_resources()
        self.TEXT = self._deep_clean(text.strip())
        self._paragraphs = None  # Кэш для разделенных абзацев

    def _ensure_nltk_resources(self):
        """Гарантирует загрузку необходимых ресурсов NLTK"""
        required_resources = ['punkt', 'russian']
        for resource in required_resources:
            try:
                nltk.data.find(f'tokenizers/punkt/{resource}.pickle' if resource != 'punkt' else 'tokenizers/punkt')
            except LookupError:
                nltk.download(resource, quiet=True)

    def _deep_clean(self, text):
        """Очистка текста от нежелательных фрагментов"""
        patterns = [
            r'Спасибо, что скачали книгу.*?',
            r'Оставить отзыв о книге.*?',
            r'Все книги автора.*?',
            r'http[s]?://\S+',
            r'Купить книгу.*?',
            r'Читать онлайн.*?',
            r'Электронная библиотека.*?',
            r'\bRoyallib\.ru\b.*?',
            r'Продолжить чтение*?'
        ]

        compiled_patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
        lines = [line for line in text.split('\n')
                 if not any(p.search(line) for p in compiled_patterns)]

        return re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip()

    def divided_paragraphs(self):
        """Разделение текста на абзацы с поиском начала главы"""
        if self._paragraphs is not None:
            return self._paragraphs

        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', self.TEXT) if p.strip()]

        for i, para in enumerate(paragraphs):
            if re.match(r'^(ГЛАВА|Глава|CHAPTER)\b', para, re.IGNORECASE):
                if i + 1 < len(paragraphs) and paragraphs[i + 1][0].islower():
                    self._paragraphs = [para + " " + paragraphs[i + 1]] + paragraphs[i + 2:]
                    return self._paragraphs
                self._paragraphs = paragraphs[i:]
                return self._paragraphs

        print("Предупреждение: Начало главы не найдено")
        self._paragraphs = paragraphs
        return self._paragraphs

    def random_fragment(self):
        ARRAY_PARAGPHS = self.divided_paragraphs()
        rand_ind = random.randint(0, len(ARRAY_PARAGPHS) - 2)
        frag = [ARRAY_PARAGPHS[rand_ind]]

        while self.count_sentences(frag) < 10:
            rand_ind += 1
            frag.append(ARRAY_PARAGPHS[rand_ind])

        return [text.replace('\xa0', ' ') for text in frag]

    def count_sentences(self, fragm_text):
        count = 0

        for text in fragm_text:
            count += text.count('.') + text.count('!') + text.count('?')

        return count