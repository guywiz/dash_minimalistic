# dash_minimalistic
Minimalistic examples of a dash application.

This repository stores versions of a minimalistic `dash` application used in a classroom context.
## Installing and running the app

First things first, you should create a dedicated environment for the app and install all required libraries as indicated in the `requirements.txt` file.

The app is then launched by simply entering the `python app_vX.py` command on a terminal (or from within your preferred IDE).

## A simple exercise

To make sure you understand how the different layout components combine, try the following:

1. Take a look at the component on line 55.
  1. Modify the value of the `width` attribute to 40%. What effect doest it have?
  2. Add a style parameter to the dcc.Graph component so it is framed with 40% of the window width.
  3. Why is the title still sitting at the extreme keft of the screen? What is a good way to fiw things so the whole app is centered on the page and sits within 40% of the window width?
