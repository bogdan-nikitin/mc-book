import streamlit as st

from text_to_book import TextToBook


@st.cache
def get_text_to_book():
    return TextToBook()


BOOK_IMAGE_URL = ('https://static.wikia.nocookie.net/'
                  'minecraft_gamepedia/images/5/50/Book_JE2_BE2.png')

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
[formatting codes](https://minecraft.fandom.com/wiki/Formatting_codes). ''')

text = st.text_area('Book text')
title = st.text_input('Book title')
author = st.text_input('Book author')

st.button('Generate')  # clicking reruns script

text_to_book = get_text_to_book()
pages = text_to_book.split_on_pages(text)

st.header('/give command')
st.text(text_to_book.generate_give_from_pages(pages, title, author))

st.header('Book pages')
for i, page in enumerate(pages):
    st.subheader(f'Page {i + 1}')
    st.text(page)
