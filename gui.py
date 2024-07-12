from tkinter import *
from tkinter import messagebox

window = Tk()
window.title("Get Subscribers App")

window.geometry('700x700')
frame = Frame(
   window,
   padx=10,
   pady=10
)
frame.pack(expand=True)
 
 
height_lb = Label(
   frame,
   text="Введите свой рост (в см)  "
)
height_lb.grid(row=3, column=1)
 
weight_lb = Label(
   frame,
   text="Введите свой вес (в кг)  ",
)
weight_lb.grid(row=4, column=1)
 
height_tf = Entry(
   frame,
)
height_tf.grid(row=3, column=2, pady=5)
 
weight_tf = Entry(
   frame,
)
weight_tf.grid(row=4, column=2, pady=5)
 
cal_btn = Button(
   frame,
   text='Рассчитать ИМТ',
)
cal_btn.grid(row=5, column=2)
window.mainloop()