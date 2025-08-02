import os
import random


class TextFinder:
    @staticmethod
    def read_text(file_path):

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            print(f"Ошибка: файл {file_path} не в UTF-8 кодировке")
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {e}")
        return None

    @staticmethod
    def get_random_text(directory='./books'):
        try:
            files = [
                f.path for f in os.scandir(directory)
                if f.is_file() and f.name.endswith('.txt')
            ]

            if not files:
                print(f"В папке {directory} нет .txt файлов")
                return None

            random_file = random.choice(files)
            return TextFinder.read_text(random_file)

        except FileNotFoundError:
            print(f"Папка {directory} не найдена")
            return None