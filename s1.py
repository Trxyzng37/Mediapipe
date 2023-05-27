import tkinter as tk

def cont(count):
    print(count)
    count += 1

def open_window1():
    window1 = tk.Tk()
    window1.title("Window 1")
    count = 0
    window1.after(1, cont(count))
    window1.mainloop()

if __name__ == "__main__":
    open_window1()
