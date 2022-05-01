# Insert a Text Into a Minecraft Book

![App](https://image.prntscr.com/image/yomD0cFGRwuXYlT46Ow5BQ.png)

The project is a web application and command-line interface that allow you to 
insert large texts into books in Minecraft, by generating the /give command or 
splitting the text into pages for later copying manually.

All other text insertion utilities that I found did not take into account the 
fact that Minecraft book uses proportional font, and therefore, you need to 
divide the text not by the number of characters, but by their total width. 
You must also take into account that bold characters have a different 
width. This app takes all these factors into account and divides the text into 
pages in an optimal way.

The web application is available at the link 
https://share.streamlit.io/bogdan-nikitin/mc-book/feature/web-streamlit/web.py

## Installation and launch

To run this application, you need to install Python version 3.9 or higher and 
the Streamlit library (to run a web application). The application has the 
following entry points:
* \_\_main\_\_.py - command-line interface
* web.py - Streamlit web app

## Contributing

The application requires the character sizes from Minecraft to split the text 
into pages, but there is no data about some characters. You can contribute to 
the project by adding character size files. Go to [web application](https://share.streamlit.io/bogdan-nikitin/mc-book/feature/web-streamlit/web.py)
and enable custom characters in the sidebar on the left to learn more. In 
short, these are files containing the width of characters in pixels. You can 
send the resulting files to GitHub Issues or open a pull request.
