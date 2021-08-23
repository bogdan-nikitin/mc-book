import json
import pathlib

# TODO: Stop storing pages as a list and save them in strings instead
#  (or use lists to store lines)

SECTION_SIGN = '§'  # \u00a7

CONFIG_FILE = 'config/config.json'

# value in pixels
MAX_LINE_LEN = 114
TRAILING_SPACE_MAX_LINE_LEN = 118

MAX_LINES = 14


def load_json(file_name):
    with open(file_name) as file:
        return json.load(file)


class Config:
    def __init__(self, config_file):
        config = load_json(config_file)
        path = pathlib.Path(config_file).parent
        self.character_size = {}
        for file_name in config['character_size']:
            self.character_size |= load_json(path.joinpath(file_name))


class DefaultConfig(Config):
    def __init__(self):
        super().__init__(CONFIG_FILE)


class TextToBook:
    """
    A class for inserting text into a Minecraft book.
    """

    def __init__(self, config=None):
        self._config = config or DefaultConfig()

    def get_char_len(self, char, is_bold):
        # all (I hope) bold characters are 1 pixel wider than normal
        return self._config.character_size[char] + (2 if is_bold else 1)

    def get_word_len(self, word, is_bold):
        return sum(self.get_char_len(char, is_bold) for char in word)

    def split_on_pages(self, text):
        pages = [[]]
        line_len = 0
        lines_count = 1
        parts = self.__split_on_parts(text)
        section = ''
        is_bold = False
        for part in parts:
            if part.startswith(SECTION_SIGN):
                modifier = part[1:]
                if modifier == 'r':
                    is_bold = False
                    section = ''
                elif self._is_color_modifier(modifier):
                    # color section resets everything for some reason
                    is_bold = False
                    section = part
                else:
                    if modifier == 'l':
                        is_bold = True
                    section += part
                pages[-1] += part
            elif part == '\n':
                # a newline can be inserted even if the lines count is maximum
                pages[-1] += ['\n']
                lines_count += 1
                if lines_count > MAX_LINES:
                    pages += [[section]]
                    lines_count = 1
                line_len = 0
            else:
                word_len = self.get_word_len(part, is_bold)
                if word_len > MAX_LINE_LEN:
                    word_parts, last_part_len = (
                        self.__split_big_word_and_get_last_len(part, is_bold)
                    )
                    if line_len == 0:
                        lines_count -= 1
                    for word_part in word_parts:
                        lines_count += 1
                        if lines_count > MAX_LINES:
                            pages += [[section]]
                            lines_count = 1
                        pages[-1] += [word_part]
                    line_len = last_part_len
                else:
                    if part == ' ':
                        max_line_len = TRAILING_SPACE_MAX_LINE_LEN
                    else:
                        max_line_len = MAX_LINE_LEN
                    if line_len + word_len > max_line_len:
                        line_len = word_len
                        lines_count += 1
                        if lines_count > MAX_LINES:
                            pages += [[section]]
                            lines_count = 1
                    else:
                        line_len += word_len
                    pages[-1] += [part]
        return list(map(self.__join_parts, pages))

    def generate_give(self, text, title, author):
        """
        Generates book /give command with the specified text, title and author
        """
        pages = self.split_on_pages(text)
        return self.generate_give_from_pages(pages, title, author)

    @staticmethod
    def generate_give_from_pages(pages, title, author):
        """
        Generates book /give command with the specified pages, title and author

        If you need to generate a book from text, use generate_give() instead
        """
        pages_json = [json.dumps({'text': page}) for page in pages]
        return (f'/give @p written_book{{pages:{pages_json},'
                f'title:{repr(title)},author:{repr(author)}}}')

    @staticmethod
    def _is_color_modifier(modifier):
        # info from https://minecraft.fandom.com/wiki/Formatting_codes
        return modifier.isdigit() or modifier in 'abcdefg'

    @staticmethod
    def __split_on_parts(text):
        # parts are sections, newlines and spaces
        parts = []
        last_word = ''
        is_last_section = False
        for char in text:
            if is_last_section:
                parts += [last_word + char]
                last_word = ''
                is_last_section = False
            elif char == SECTION_SIGN:
                if last_word:
                    parts += [last_word]
                last_word = SECTION_SIGN
                is_last_section = True
            elif char == ' ' or char == '\n':
                if last_word:
                    parts += [last_word]
                last_word = ''
                parts += [char]
            elif char == SECTION_SIGN:
                if last_word:
                    parts += [last_word]
                last_word = char
            else:
                last_word += char
        if last_word:
            parts += [last_word]
        return parts

    @staticmethod
    def __join_parts(parts):
        return ''.join(parts)

    def __split_big_word_and_get_last_len(self, word, is_bold):
        parts = ['']
        last_part_len = 0
        for char in word:
            char_len = self.get_char_len(char, is_bold)
            if last_part_len + char_len > MAX_LINE_LEN:
                parts += ['']
                last_part_len = 0
            parts[-1] += char
            last_part_len += char_len
        return parts, last_part_len

# def generate_give_writable(text):
#     pages = split_on_pages(text)
#     pages = [json.dumps(page).strip('"') for page in pages]
#     return f'/give @p writable_book{{pages:{json.dumps(pages)}}}'
