import tkinter as tk
from tkinter import *

#Logic (Model and Controller)
def convert_celsius_to_f():
    celsius_string = celsius_var.get()
    if not celsius_string:
        raise ValueError("Input cannot be empty")
    
    celsius = float(celsius_string)
    f_temp = (celsius * (9/5)) + 32
    f_result.set("Result: " + str(f_temp) + " °F")

#Main (View)
window = tk.Tk()
window.title("Temperature Converter")
window.grid_columnconfigure(1,weight=1)

#binding logic to controller
celsius_var = tk.StringVar()
f_result = tk.StringVar(value="Result: 0.0°F")

#Containers and Widgets (celsius_label, convert_button, result_label)
celsius_label = tk.Label(window,text="Celsius: ")
celsius_label.grid(row=0,column=0,padx=10,pady=5,sticky="EW")

celsius_entry = tk.Entry(window, textvariable=celsius_var)
celsius_entry.grid(row=0,column=1,padx=10,pady=5,sticky="EW")

convert_button = tk.Button(window,text="Convert to Fahrenheit",
                    command=convert_celsius_to_f)
convert_button.grid(row=1,column=0,columnspan=2,padx=5,pady=5,sticky="EW")

result_label = tk.Label(window, textvariable=f_result,font=("Arial",12,"bold"))
result_label.grid(row=2,column=0,columnspan=2,padx=5,pady=5)


#Start App
window.mainloop()
                                                            






