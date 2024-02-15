import tkinter as tk

root = tk.Tk()
root.geometry("500x500")
root.configure(bg='#fadd82')
root.title("Mood Visualization Project")

#The header which stays static
header = tk.Frame(master=root, bg='#fc9247')

label = tk.Label(header, text="Mood Visualization Project", bg="#f7bf31", font=('Tekton Pro', 45))
label.pack(padx=20, pady=20)

text_var = tk.StringVar()
entry = tk.Entry(header, textvariable=text_var, font=("Bell Gothic Std Light", 16))
entry.pack(padx=20, pady=20)

header.pack(fill='x')

#Variables
def get_input(event):
    text = text_var.get()
    print(text)
    text_var.set("")
    return text
entry.bind('<Return>', get_input)




root.mainloop()

