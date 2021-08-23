import pathlib
import unittest

from text_to_book import TextToBook, Config

# Some tests for big words may be unnecessary


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
        """
        Tests split_on_pages() for texts, located in ./text_files

        All texts must have next format:

        % text to split %
        ^^^
        % page 1 of the split text %
        @@@
        % page 2 %
        @@@
        % page 3 %
        @@@
        % page N %

        Don't forget about trailing newlines in texts
        """
        for file_name in TEXT_FILES_PATH.iterdir():
            with self.subTest(file_name=file_name):
                text_to_book = TextToBook(CONFIG)
                text, text_split = load_text_test(file_name)
                self.assertSequenceEqual(text_split,
                                         text_to_book.split_on_pages(text))


if __name__ == '__main__':
    unittest.main()
