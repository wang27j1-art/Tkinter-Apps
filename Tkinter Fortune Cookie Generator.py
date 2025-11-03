import tkinter as tk
from tkinter import *
import random

#Logic (Model and Controller)
def generate_quote():
    new_quote = random.choice(QUOTES)
    #Controller talking to Model
    quote_var.set(new_quote)


#Main (View)
window = Tk()
window.title("Fortune Cookie Generator")
window.geometry("550x250")
window.config(padx=10,pady=10,bg="#c0d8e3")


QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Strive not to be a success, but rather to be of value. - Albert Einstein",
    "In the middle of every difficulty lies opportunity. - Albert Einstein",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "Live more. Laugh more. Eat more. Talk more. - Gilmore.",
    "Life's short. Talk fast. - Lorelai",
    "It’s times like these that you realize what’s truly important in your life. - Miss Patty",
    "You have family. You have friends. You have people to talk to. - Rory",
    "I would rather have thirty minutes of wonderful than a lifetime of nothing special - Shelby",
    "Laughter through tears is my favorite emotion. - Truvy",
    "My mama always said life was like a box of chocolates. You never know what you’re gonna get. — Forrest Gump",
    "You're braver than you believe, stronger than you seem, and smarter than you think. - Winnie the Pooh",
    "Sometimes the smallest things take up the most room in your heart. - Winnie the Pooh",
    "Any day spent with you is my favorite day. - Winnie the Pooh"
]

quote_var = StringVar(window) #Controller talking to View
generator_button = Button(window,
                          text="New Quote",
                          command=generate_quote,
                          font=("Arial",18,"bold"),
                          bg="white",
                          fg="#b44000",
                          padx=5,
                          )

generator_button.pack(pady=10)
quote_label = Label(window,
                    textvariable=quote_var, #controller to model
                    font=("Georgia",18,"italic"),
                    wraplength=500,
                    justify=tk.CENTER,
                    bg="white",
                    fg="#b44000")
quote_label.pack(pady=(20,30),fill=tk.X)

#Start App
window.mainloop()
