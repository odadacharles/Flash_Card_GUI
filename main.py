from tkinter import *
import pandas as pd
from random import choice
DELAY = 3000
display_line = {}

# -------------------------- Access Data in CSV file ---------------------- #
try:
    data = pd.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    data = pd.read_csv('data/french_words.csv')
finally:
    french_word_list = data.to_dict(orient="records")

# ------------------------ Choose and translate words ---------------------- #


def next_card(button):
    global flip_timer, display_line
    window.after_cancel(flip_timer)
    if button == "known":
        french_word_list.remove(display_line)
        to_learn_df = pd.DataFrame(french_word_list)
        to_learn_df.to_csv('data/words_to_learn.csv', index=False)
        print(len(french_word_list))
    else:
        pass
    display_line = choice(french_word_list)
    french_word = display_line['French']
    canvas.itemconfig(card_face, image=card_front)
    canvas.itemconfig(title, text='French', fill='black')
    canvas.itemconfig(word, text=french_word, fill='black')
    flip_timer = window.after(3000, translate, display_line)


def translate(line):
    english_word = line['English']
    canvas.itemconfig(card_face, image=card_back)
    canvas.itemconfig(title, text='English', fill='white')
    canvas.itemconfig(word, text=english_word, fill='white')


# ---------------------------- UI SETUP --------------------------------------- #
# color scheme
BACKGROUND_COLOR = "#B1DDC6"
FONT1 = ("Georgia", 40, 'italic')
FONT2 = ("Georgia", 45, 'bold')

# window
window = Tk()
window.title('Flash Cards')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, translate, display_line)

# Canvas
card_front = PhotoImage(file='images/card_front.png')
card_back = PhotoImage(file='images/card_back.png')
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_face = canvas.create_image(400, 263, image=card_front)
title = canvas.create_text(400, 210, text="Title", font=FONT1)
word = canvas.create_text(400, 270, text="Word", font=FONT2)
canvas.grid(column=0, row=0, sticky='ew', columnspan=2)

# Check-mark button
check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=lambda k="known": next_card(k))
known_button.grid(column=1, row=1)

# Unknown (X) button
unknown_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=unknown_image, highlightthickness=0, command=lambda u="unknown": next_card(u))
unknown_button.grid(column=0, row=1)
next_card("")

window.mainloop()

