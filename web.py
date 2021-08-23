import streamlit as st
import json
from text_to_book import TextToBook, CharError


@st.cache(allow_output_mutation=True)
def get_text_to_book():
    return TextToBook()


@st.cache
def extend_config(character_size_file):
    character_size = json.load(character_size_file)
    get_text_to_book().config.extend(character_size)


BOOK_IMAGE_URL = ('https://static.wikia.nocookie.net/'
                  'minecraft_gamepedia/images/5/50/Book_JE2_BE2.png')
GITHUB_ISSUES_URL = 'https://github.com/bogdan-nikitin/mc-book/issues/new'
GITHUB_ISSUES_LINK = f'[Github Issues]({GITHUB_ISSUES_URL})'

st.set_page_config('Insert Into Minecraft Book', BOOK_IMAGE_URL)

# App presentation
st.title('Insert a Text Into a Minecraft Book')
st.image(BOOK_IMAGE_URL)
st.markdown('''
This app will help you insert a large text into a Minecraft book. Paste your 
text, click "Generate" and copy the "/give" command to the command block or 
chat. Or you can manually copy the pages to your book (if you can't use the 
"/give" command).

To make the font bold or add color, you can use 
[formatting codes](https://minecraft.fandom.com/wiki/Formatting_codes). 
''')

text = st.text_area('Book text')
title = st.text_input('Book title')
author = st.text_input('Book author')

st.button('Generate')  # clicking reruns script

text_to_bark = get_text_to_book()
have_char_error = False
try:
    pages = text_to_bark.split_on_pages(text)

    st.header('/give command')
    st.text(text_to_bark.generate_give_from_pages(pages, title, author))

    st.header('Book pages')
    for i, page in enumerate(pages):
        st.subheader(f'Page {i + 1}')
        st.text(page)
except CharError as er:
    st.error(f'Size of character "{er.char}" is unknown. '
             f'[Learn more](#custom-characters) ')
    have_char_error = True
except Exception as e:
    st.error(f'''
Exception "{e.__class__.__name__}" was raised. Go to {GITHUB_ISSUES_LINK} to
report your problem. Specify the exception, text, book title, author, and other
parameters entered on the page.
    ''')


st.markdown('---')
if not have_char_error:
    st.info('''
The information below is intended for people who have an error while using the 
application
    ''')
# Custom characters info
st.header('Custom characters')
st.markdown('''
The application requires the character sizes from Minecraft to divide the text 
into pages, but there is no data about some characters, so an error may occur 
while the application is running.
''')
st.subheader('Fixing the error')
st.markdown(f'''
First, please let us know on {GITHUB_ISSUES_LINK} which character you have a 
problem with. Then, you can set a default character size (but this will worsen 
the quality of text splitting) or upload a file with character sizes below.
''')
st.subheader('File format')
st.markdown('''
The file must have a JSON extension, characters must be specified as keys, and 
numbers corresponding to the size of characters must be specified as values. 
For example, if you wanted to add support for the symbols α, β and γ, you would 
need to upload a file with the following content:
''')
st.json({"α": 5, "β": 5, "γ": 5})
st.subheader('Finding the size of characters')
st.markdown('''
To find out the size of symbols, go to Minecraft, take a Book and Quill and 
insert the symbols. Count their width in pixels. You need to specify these 
values in the file
''')
st.image('https://i.imgur.com/4NbISjj.jpeg')
st.markdown('''
Some characters consist of smaller pixels (for example, "ϖ"). When finding its 
size, you will need to match it with a normal-sized character and specify its 
width. For example, the width of "ϖ" is the same as the width of "t", so you 
will need to specify 3 as the width.
''')
st.header('Configure custom characters')
use_default_size = st.checkbox('Use default size for unknown characters')
if use_default_size:
    # 4 is medium value
    default_size = st.number_input(
        'Default character size', 0, step=1, value=4
    )  # TODO
character_size_files = st.file_uploader('Character size file', 'json', True)
for file in character_size_files:
    extend_config(file)
if character_size_files:
    st.info(f'''
Please post your character size files on {GITHUB_ISSUES_LINK} so that we can 
make them available to everyone by default!
    ''')
