import tkinter as tk
from tkinter import *
import random

#Logic (Model and Controller)
def generate_secret_number(start, end):
    secret_num = random.randint(start, end)
    return secret_num

random_num = generate_secret_number(1, 100)

def check_guess():
    global random_num
    input_num_str = input_num.get()
    if not input_num_str:
        num_result.set("Input cannot be empty")
        return

    try:
        num = int(input_num_str)
    except ValueError:
        num_result.set("Please ente a valid integer.")
        return
    
    if num == random_num:
        num_result.set("You got it! Congratulations")
        secret_number = generate_secret_number(1, 100)
    elif num >= random_num:
        num_result.set("Too high! Try again.")
    else:
        num_result.set("Too low! Try again.")


#Main (View)
window = tk.Tk()
window.title("Guess the number!")
window.grid_columnconfigure(1,weight=1)

#binding logic to controller
input_num = tk.StringVar()
num_result = tk.StringVar(value="I have a new number! Guess it!")

#Containers and Widgets
instruction_label = tk.Label(window,text="I'm thinking of a number between 1 and 100")
instruction_label.grid(row=0, column=0,padx=10,pady=5,sticky="EW")

entry = tk.Entry(window, textvariable=input_num)
entry.grid(row=1,column=0,padx=10,pady=5)

check_button = tk.Button(window,text="Guess",
                         command=check_guess)
check_button.grid(row=2,column=0,columnspan=2,padx=5,pady=5)

result_label = tk.Label(window, textvariable=num_result,font=("Arial",12,"bold"))
result_label.grid(row=3,column=0,columnspan=2,padx=5,pady=5)

#Start app
window.mainloop()

