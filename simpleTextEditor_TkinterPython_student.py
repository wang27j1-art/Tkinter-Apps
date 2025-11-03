import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file():
    """Open a file for editing using the tkinter.filedialog module"""
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])

    # ADD STUDENT CODE
    if not filepath:
        return
    
    text_edit.delete("1.0", tk.END)
    
    try:
        with open(filepath, 'r') as file:
            text = file.read()
            text_edit.insert(tk.END, text)
    except FileNotFoundError:
        print("Error: The file was not found")
    
    text_edit.insert(tk.END, text)
                     



    

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(defaultextension=".txt",filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],)

    # ADD STUDENT CODE
    if not filepath:
        return
    
    try:
        with open(filepath, "w") as output_file:
            text = text_edit.get("1.0", tk.END)
            output_file.write(text)
    except FileNotFoundError:
        print("Error: File not found")
    


    

window=tk.Tk()
window.title("Simple Text Editor")
window.geometry("800x500")
window.grid_columnconfigure(1,weight=1)

# ADD STUDENT CODE
frame_buttons = tk.Frame(window,relief=tk.RAISED,bd=1)
frame_buttons.grid(column=0,row=0,padx=10,pady=5,sticky="NS")
button_open = tk.Button(frame_buttons,text="Open",command=open_file,padx=5)
button_open.grid(column=0,row=0,padx=10,pady=5)
button_save = tk.Button(frame_buttons,text="Save As",command=save_file,padx=5)
button_save.grid(column=0,row=1,padx=10,pady=5)


text_edit = tk.Text(window)
text_edit.grid(column=1,row=0,padx=10,pady=5,sticky="NSEW")


# START APP
window.mainloop()
