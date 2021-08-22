import pathlib
import unittest

from text_to_book import TextToBook, Config

# Don't forget about trailing newlines in tests!


TEXT_FILE_DELIMITER = '\n^^^\n'
TEXT_FILE_PAGE_DELIMITER = '\n@@@\n'

CONFIG = Config('../config/config.json')
TEXT_FILES_PATH = pathlib.Path('./text_files')


def load_text_test(file_name):
    with open(file_name) as file:
        text, text_split = file.read().split(TEXT_FILE_DELIMITER)
        text_split = text_split.split(TEXT_FILE_PAGE_DELIMITER)
    return text, text_split


class TestPagesSplit(unittest.TestCase):
    def test_text_files(self):
        for file_name in TEXT_FILES_PATH.iterdir():
            with self.subTest(file_name=file_name):
                text_to_book = TextToBook(CONFIG)
                text, text_split = load_text_test(file_name)
                self.assertEqual(text_split, text_to_book.split_on_pages(text))


if __name__ == '__main__':
    unittest.main()
