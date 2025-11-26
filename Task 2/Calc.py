# TASK 2
# Basic arithmetic calculator with user input
# Developed by: Akansh Jadam
# Internship Task – CodSoft (Python Programming Intern)
# Date: 26/NOV/2025


import tkinter as tk
from tkinter import messagebox

class Calc:
    def __init__(self, root):
        self.root = root
        self.root.title("My Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        self.bg_color = "#471313"     
        self.btn_color = "#004183"    
        self.text_color = "#FFFFFF"   
        self.accent_color = "#503805" 
        
        self.root.configure(bg=self.bg_color)
        
        self.expression = ""
        self.input_text = tk.StringVar()
        
        input_frame = tk.Frame(self.root, width=312, height=50, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        input_frame.pack(side=tk.TOP)
        
        input_field = tk.Entry(input_frame, font=('arial', 18, 'bold'), textvariable=self.input_text, width=50, bg="#ecf0f1", bd=0, justify=tk.RIGHT)
        input_field.grid(row=0, column=0)
        input_field.pack(ipady=10)

        btns_frame = tk.Frame(self.root, width=312, height=322.5, bg=self.bg_color)
        btns_frame.pack()
        
    
        self.create_btn(btns_frame, "C", 1, 0, 3, lambda: self.btn_clear(), "#9E1A0C")
        self.create_btn(btns_frame, "/", 1, 3, 1, lambda: self.btn_click("/"))
        
        self.create_btn(btns_frame, "7", 2, 0, 1, lambda: self.btn_click(7))
        self.create_btn(btns_frame, "8", 2, 1, 1, lambda: self.btn_click(8))
        self.create_btn(btns_frame, "9", 2, 2, 1, lambda: self.btn_click(9))
        self.create_btn(btns_frame, "*", 2, 3, 1, lambda: self.btn_click("*"))
        
        self.create_btn(btns_frame, "4", 3, 0, 1, lambda: self.btn_click(4))
        self.create_btn(btns_frame, "5", 3, 1, 1, lambda: self.btn_click(5))
        self.create_btn(btns_frame, "6", 3, 2, 1, lambda: self.btn_click(6))
        self.create_btn(btns_frame, "-", 3, 3, 1, lambda: self.btn_click("-"))
        
        self.create_btn(btns_frame, "1", 4, 0, 1, lambda: self.btn_click(1))
        self.create_btn(btns_frame, "2", 4, 1, 1, lambda: self.btn_click(2))
        self.create_btn(btns_frame, "3", 4, 2, 1, lambda: self.btn_click(3))
        self.create_btn(btns_frame, "+", 4, 3, 1, lambda: self.btn_click("+"))
       
        self.create_btn(btns_frame, "0", 5, 0, 2, lambda: self.btn_click(0))
        self.create_btn(btns_frame, ".", 5, 2, 1, lambda: self.btn_click("."))
        self.create_btn(btns_frame, "=", 5, 3, 1, lambda: self.btn_equal(), self.accent_color)
        
    def create_btn(self, frame, text, row, col, width, command, bg_color=None):
        if bg_color is None:
            bg_color = self.btn_color
            
        tk.Button(frame, text=text, fg="white", width=width*10, height=3, bd=0, bg=bg_color, cursor="hand2",
                  command=command).grid(row=row, column=col, padx=1, pady=1, sticky="nsew", columnspan=width)

    def btn_click(self, item):
        self.expression = self.expression + str(item)
        self.input_text.set(self.expression)

    def btn_clear(self):
        self.expression = ""
        self.input_text.set("")

    def btn_equal(self):
        try:
            result = str(eval(self.expression)) 
            self.input_text.set(result)
            self.expression = result
        except:
            self.input_text.set("Error")
            self.expression = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = Calc(root)
    root.mainloop()