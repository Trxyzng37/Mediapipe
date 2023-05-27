import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image  

def mainx(queue):
    count = 0
    def print_count(count):
        count += 1
        print(count)

    def toggle_image(button):
        current_image = button.current_image
        if current_image == bulb_off:
            new_image = bulb_on
        if current_image == bulb_on:
            new_image = bulb_off
        button.config(image=new_image)
        button.current_image = new_image

    def switch_to_room1(room1_btn, room2_btn):
        room1_frame.tkraise()
        new_room1_btn_img = living_room_on
        room1_btn.config(image=new_room1_btn_img)
        room1_btn.current_image = new_room1_btn_img
        new_room2_btn_img = bedroom_off
        room2_btn.config(image=new_room2_btn_img)
        room2_btn.current_image = new_room2_btn_img
        
    def switch_to_room2(room1_btn, room2_btn):    
        room2_frame.tkraise()
        new_room1_btn_img = living_room_off
        room1_btn.config(image=new_room1_btn_img)
        room1_btn.current_image = new_room1_btn_img
        new_room2_btn_img = bedroom_on
        room2_btn.config(image=new_room2_btn_img)
        room2_btn.current_image = new_room2_btn_img


    #define the window
    window = tk.Tk()
    window.title("ELECTRONIC DEVICES CONTROL SYSTEM USING HAND GESTURE RECOGNITION")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    #window.resizable(False,False)
    window.config(bg="white")
    print(str(screen_width)+"|"+str(screen_height))
    # Add padding to the window
    window.padding = 10
    window.configure(padx=window.padding, pady=window.padding)

    #style the combobox arrow size
    style = ttk.Style() 
    style.configure('TCombobox', arrowsize=30)
    style.configure('Vertical.TScrollbar', arrowsize=30)
    #change combobox inside font
    bigfont = ("Helvetica",20)
    window.option_add("*TCombobox*Listbox*Font", bigfont)

    #define image use for tkinter#######################################################
    bulb_off = Image.open("img/light_off.png")
    bulb_off = bulb_off.resize((200,200), Image.LANCZOS)
    bulb_off = ImageTk.PhotoImage(bulb_off)

    bulb_on = Image.open("img/light_on.png")
    bulb_on = bulb_on.resize((200,200), Image.LANCZOS)
    bulb_on = ImageTk.PhotoImage(bulb_on)

    bedroom_on = Image.open("img/bedroom_on.png")
    bedroom_on = bedroom_on.resize((90,100), Image.LANCZOS)
    bedroom_on = ImageTk.PhotoImage(bedroom_on)

    bedroom_off = Image.open("img/bedroom_off.png")
    bedroom_off = bedroom_off.resize((90,100), Image.LANCZOS)
    bedroom_off = ImageTk.PhotoImage(bedroom_off)

    living_room_off = Image.open("img/living_room_off.png")
    living_room_off = living_room_off.resize((90,100), Image.LANCZOS)
    living_room_off = ImageTk.PhotoImage(living_room_off)

    living_room_on = Image.open("img/living_room_on.png")
    living_room_on = living_room_on.resize((90,100), Image.LANCZOS)
    living_room_on = ImageTk.PhotoImage(living_room_on)
    ###################################################################################

    # create main frame for window
    choice_frame = tk.Frame(window)
    choice_frame.grid(row=0, column=0, sticky="nsew")
    # create frame for room 1
    room1_frame = tk.Frame(window)
    room1_frame.grid(row=0, column=1, sticky="nsew")
    # create frame for room 2
    room2_frame = tk.Frame(window)
    room2_frame.grid(row=0, column=1, sticky="nsew")

    room1_frame.tkraise()

    # Update grid configuration for grid of window
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=2)
    window.grid_columnconfigure(1, weight=3)  # Changed weight to 3 for right frame

    # grid for choice frame
    choice_frame.grid_rowconfigure(0, weight=1)
    choice_frame.grid_rowconfigure(1, weight=1)  
    choice_frame.grid_columnconfigure(0, weight=1)

    # grid for room 1
    room1_frame.grid_rowconfigure(0, weight=1)
    room1_frame.grid_rowconfigure(1, weight=2)
    room1_frame.grid_columnconfigure(0, weight=1)
    room1_frame.grid_columnconfigure(1, weight=1)
    room1_frame.grid_columnconfigure(2, weight=1)
    room1_frame.grid_columnconfigure(3, weight=1)
    room1_frame.grid_columnconfigure(4, weight=1)

    #grid for room 2
    room2_frame.grid_rowconfigure(0, weight=1)
    room2_frame.grid_rowconfigure(1, weight=2)
    room2_frame.grid_columnconfigure(0, weight=1)
    room2_frame.grid_columnconfigure(1, weight=1)
    room2_frame.grid_columnconfigure(2, weight=1)
    room2_frame.grid_columnconfigure(3, weight=1)
    room2_frame.grid_columnconfigure(4, weight=1)


    # button for switch room 
    button1 = tk.Button(choice_frame, image=living_room_on, compound=tk.CENTER, bg="white")
    button1.current_image = living_room_on
    button2 = tk.Button(choice_frame, image=bedroom_off, compound=tk.CENTER, bg="white")
    button2.current_image = bedroom_off

    button1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    button1.configure(command=lambda btn2=button2, btn1=button1: switch_to_room1(btn1,btn2))
    button2.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    button2.configure(command=lambda btn2=button2, btn1=button1: switch_to_room2(btn1,btn2))


    #room1 frame###############################
    # Merge cells in the device frame and add text
    label = ttk.Label(room1_frame, text="HOẶC CHÍ TRUNG - NGUYỄN GIA HƯNG\n ELECTRONIC DEVICES CONTROL SYSTEM USING HAND GESTURE RECOGNITION\nHCMUTE", font=("Arial", 8), anchor="center", justify="center")
    label.grid(row=0, column=1, ipadx=0, ipady=10, padx=5, pady=5, sticky="nsew", columnspan=4)
    label.configure(background="white")

    def room1_1_1(event):
        selected_value = room1_cbbox_1_1.get()
        if selected_value == 'One':
            image_path = f"img/One.png"
        elif selected_value == 'Two':
            image_path = 'img/Two.png'
        elif selected_value == 'Three':
            image_path = 'img/Three.png'
        elif selected_value == 'Four':
            image_path = 'img/Four.png'
        elif selected_value == 'Five':
            image_path = 'img/Five.png'
        elif selected_value == 'Six':
            image_path = 'img/Six.png'
        elif selected_value == 'Seven':
            image_path = 'img/Seven.png'
        elif selected_value == 'Eight':
            image_path = 'img/Eight.png'
        else:
            image_path = 'img/light_off.png'

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        room1_img_1_1.configure(image=current_image)
        room1_img_1_1.image = current_image
        print(selected_value)

    def room1_1_2(event):
        selected_value = room1_cbbox_1_2.get()
        if selected_value == 'One':
            image_path = f"img/One.png"
        elif selected_value == 'Two':
            image_path = 'img/Two.png'
        elif selected_value == 'Three':
            image_path = 'img/Three.png'
        elif selected_value == 'Four':
            image_path = 'img/Four.png'
        elif selected_value == 'Five':
            image_path = 'img/Five.png'
        elif selected_value == 'Six':
            image_path = 'img/Six.png'
        elif selected_value == 'Seven':
            image_path = 'img/Seven.png'
        elif selected_value == 'Eight':
            image_path = 'img/Eight.png'
        else:
            image_path = 'img/light_off.png'

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        room1_img_1_2.configure(image=current_image)
        room1_img_1_2.image = current_image
        print(selected_value)

    def room1_1_3(event):
        selected_value = room1_cbbox_1_3.get()
        if selected_value == 'One':
            image_path = f"img/One.png"
        elif selected_value == 'Two':
            image_path = 'img/Two.png'
        elif selected_value == 'Three':
            image_path = 'img/Three.png'
        elif selected_value == 'Four':
            image_path = 'img/Four.png'
        elif selected_value == 'Five':
            image_path = 'img/Five.png'
        elif selected_value == 'Six':
            image_path = 'img/Six.png'
        elif selected_value == 'Seven':
            image_path = 'img/Seven.png'
        elif selected_value == 'Eight':
            image_path = 'img/Eight.png'
        else:
            image_path = 'img/light_off.png'

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        room1_img_1_3.configure(image=current_image)
        room1_img_1_3.image = current_image
        print(selected_value)

    def room1_1_4(event):
        selected_value = room1_cbbox_1_4.get()
        if selected_value == 'One':
            image_path = f"img/One.png"
        elif selected_value == 'Two':
            image_path = 'img/Two.png'
        elif selected_value == 'Three':
            image_path = 'img/Three.png'
        elif selected_value == 'Four':
            image_path = 'img/Four.png'
        elif selected_value == 'Five':
            image_path = 'img/Five.png'
        elif selected_value == 'Six':
            image_path = 'img/Six.png'
        elif selected_value == 'Seven':
            image_path = 'img/Seven.png'
        elif selected_value == 'Eight':
            image_path = 'img/Eight.png'
        else:
            image_path = 'img/light_off.png'

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        room1_img_1_4.configure(image=current_image)
        room1_img_1_4.image = current_image
        print(selected_value)

    def room2_2_1(event):
        selected_value = room2_cbbox_2_1.get()
        if selected_value == 'One':
            image_path = f"img/One.png"
        elif selected_value == 'Two':
            image_path = 'img/Two.png'
        elif selected_value == 'Three':
            image_path = 'img/Three.png'
        elif selected_value == 'Four':
            image_path = 'img/Four.png'
        elif selected_value == 'Five':
            image_path = 'img/Five.png'
        elif selected_value == 'Six':
            image_path = 'img/Six.png'
        elif selected_value == 'Seven':
            image_path = 'img/Seven.png'
        elif selected_value == 'Eight':
            image_path = 'img/Eight.png'
        else:
            image_path = 'img/light_off.png'

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        room2_img_2_1.configure(image=current_image)
        room2_img_2_1.image = current_image
        print(selected_value)

    def room2_2_2(event):
        selected_value = room2_cbbox_2_2.get()
        if selected_value == 'One':
            image_path = f"img/One.png"
        elif selected_value == 'Two':
            image_path = 'img/Two.png'
        elif selected_value == 'Three':
            image_path = 'img/Three.png'
        elif selected_value == 'Four':
            image_path = 'img/Four.png'
        elif selected_value == 'Five':
            image_path = 'img/Five.png'
        elif selected_value == 'Six':
            image_path = 'img/Six.png'
        elif selected_value == 'Seven':
            image_path = 'img/Seven.png'
        elif selected_value == 'Eight':
            image_path = 'img/Eight.png'
        else:
            image_path = 'img/light_off.png'

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        room2_img_2_2.configure(image=current_image)
        room2_img_2_2.image = current_image
        print(selected_value)

    def room2_2_3(event):
        selected_value = room2_cbbox_2_3.get()
        if selected_value == 'One':
            image_path = f"img/One.png"
        elif selected_value == 'Two':
            image_path = 'img/Two.png'
        elif selected_value == 'Three':
            image_path = 'img/Three.png'
        elif selected_value == 'Four':
            image_path = 'img/Four.png'
        elif selected_value == 'Five':
            image_path = 'img/Five.png'
        elif selected_value == 'Six':
            image_path = 'img/Six.png'
        elif selected_value == 'Seven':
            image_path = 'img/Seven.png'
        elif selected_value == 'Eight':
            image_path = 'img/Eight.png'
        else:
            image_path = 'img/light_off.png'

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        room2_img_2_3.configure(image=current_image)
        room2_img_2_3.image = current_image
        print(selected_value)

    def room2_2_4(event):
        selected_value = room2_cbbox_2_4.get()
        if selected_value == 'One':
            image_path = f"img/One.png"
        elif selected_value == 'Two':
            image_path = 'img/Two.png'
        elif selected_value == 'Three':
            image_path = 'img/Three.png'
        elif selected_value == 'Four':
            image_path = 'img/Four.png'
        elif selected_value == 'Five':
            image_path = 'img/Five.png'
        elif selected_value == 'Six':
            image_path = 'img/Six.png'
        elif selected_value == 'Seven':
            image_path = 'img/Seven.png'
        elif selected_value == 'Eight':
            image_path = 'img/Eight.png'
        else:
            image_path = 'img/light_off.png'

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        room2_img_2_4.configure(image=current_image)
        room2_img_2_4.image = current_image
        print(selected_value)

    #row 1, col 1
    room1_cbbox_1_1_str = tk.StringVar()
    room1_frame_1_1 = tk.Frame(room1_frame, borderwidth=2, relief="solid", background="white")
    room1_btn_1_1 = tk.Button(room1_frame_1_1, image=bulb_off, bg="white", fg="white")
    room1_btn_1_1.current_image = bulb_off
    room1_btn_1_1.configure(command=lambda btn=room1_btn_1_1: toggle_image(btn))
    room1_btn_1_1.pack(side="top", ipadx=5, ipady=5)
    room1_cbbox_1_1 = ttk.Combobox(room1_frame_1_1, font="Verdana 20 bold", width=5, justify="center", textvariable=room1_cbbox_1_1_str, state="readonly", values=("One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Eleven","Twelve"))
    room1_cbbox_1_1.pack(anchor="n", pady=10) 
    room1_cbbox_1_1.set("One")
    room1_cbbox_1_1.bind('<<ComboboxSelected>>', room1_1_1)
    room1_img_1_1 = ttk.Label(room1_frame_1_1, image=living_room_on)
    room1_img_1_1.config(anchor='center')
    room1_img_1_1.pack( expand=True)
    room1_img_1_1.configure(background="white")
    room1_frame_1_1.grid(row=1,column=1,sticky="nsew", padx=5,pady=5)
    #row 1, col 2
    room1_cbbox_1_2_str = tk.StringVar()
    room1_frame_1_2 = tk.Frame(room1_frame, borderwidth=2, relief="solid", background="white")
    room1_btn_1_2 = tk.Button(room1_frame_1_2, image=bulb_off, bg="white", fg="white")
    room1_btn_1_2.current_image = bulb_off
    room1_btn_1_2.configure(command=lambda btn=room1_btn_1_2: toggle_image(btn))
    room1_btn_1_2.pack(side="top", ipadx=5, ipady=5)
    room1_cbbox_1_2 = ttk.Combobox(room1_frame_1_2, font="Verdana 20 bold", width=5, justify="center", textvariable=room1_cbbox_1_2_str, state="readonly", values=("One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Eleven","Twelve"))
    room1_cbbox_1_2.pack(anchor="n", pady=10) 
    room1_cbbox_1_2.set("Two")
    room1_cbbox_1_2.bind('<<ComboboxSelected>>', room1_1_2)
    room1_img_1_2 = ttk.Label(room1_frame_1_2, image=living_room_on)
    room1_img_1_2.config(anchor='center')
    room1_img_1_2.pack( expand=True)
    room1_img_1_2.configure(background="white")
    room1_frame_1_2.grid(row=1,column=2,sticky="nsew", padx=5,pady=5)

    #row 1, col 3
    room1_cbbox_1_3_str = tk.StringVar()
    room1_frame_1_3 = tk.Frame(room1_frame, borderwidth=2, relief="solid", background="white")
    room1_btn_1_3 = tk.Button(room1_frame_1_3, image=bulb_off, bg="white", fg="white")
    room1_btn_1_3.current_image = bulb_off
    room1_btn_1_3.configure(command=lambda btn=room1_btn_1_3: toggle_image(btn))
    room1_btn_1_3.pack(side="top", ipadx=5, ipady=5)
    room1_cbbox_1_3 = ttk.Combobox(room1_frame_1_3, font="Verdana 20 bold", width=5, justify="center", textvariable=room1_cbbox_1_3_str, state="readonly", values=("One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Eleven","Twelve"))
    room1_cbbox_1_3.pack(anchor="n", pady=10) 
    room1_cbbox_1_3.set("Three")
    room1_cbbox_1_3.bind('<<ComboboxSelected>>', room1_1_3)
    room1_img_1_3 = ttk.Label(room1_frame_1_3, image=living_room_on)
    room1_img_1_3.config(anchor='center')
    room1_img_1_3.pack( expand=True)
    room1_img_1_3.configure(background="white")
    room1_frame_1_3.grid(row=1,column=3,sticky="nsew", padx=5,pady=5)
    #row 1, col 4
    room1_cbbox_1_4_str = tk.StringVar()
    room1_frame_1_4 = tk.Frame(room1_frame, borderwidth=2, relief="solid", background="white")
    room1_btn_1_4 = tk.Button(room1_frame_1_4, image=bulb_off, bg="white", fg="white")
    room1_btn_1_4.current_image = bulb_off
    room1_btn_1_4.configure(command=lambda btn=room1_btn_1_4: toggle_image(btn))
    room1_btn_1_4.pack(side="top", ipadx=5, ipady=5)
    room1_cbbox_1_4 = ttk.Combobox(room1_frame_1_4, font="Verdana 20 bold", width=5, justify="center", textvariable=room1_cbbox_1_4_str, state="readonly", values=("One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Eleven","Twelve"))
    room1_cbbox_1_4.pack(anchor="n", pady=10) 
    room1_cbbox_1_4.set("Four")
    room1_cbbox_1_4.bind('<<ComboboxSelected>>', room1_1_4)
    room1_img_1_4 = ttk.Label(room1_frame_1_4, image=living_room_on)
    room1_img_1_4.config(anchor='center')
    room1_img_1_4.pack( expand=True)
    room1_img_1_4.configure(background="white")
    room1_frame_1_4.grid(row=1,column=4,sticky="nsew", padx=5,pady=5)




    ####################################room2 frame
    # Merge cells in the device frame and add text
    label = ttk.Label(room2_frame, text="HOẶC CHÍ TRUNG - NGUYỄN GIA HƯNG\n ELECTRONIC DEVICES CONTROL SYSTEM USING HAND GESTURE RECOGNITION\nHCMUTE", font=("Arial", 8), anchor="center", justify="center")
    label.grid(row=0, column=1, ipadx=0, ipady=10, padx=5, pady=5, sticky="nsew", columnspan=4)
    label.configure(background="white")

    #row 1, col 1
    room2_cbbox_2_1_str = tk.StringVar()
    room2_frame_2_1 = tk.Frame(room2_frame, borderwidth=2, relief="solid", background="white")
    room2_btn_2_1 = tk.Button(room2_frame_2_1, image=bulb_off, bg="white", fg="white")
    room2_btn_2_1.current_image = bulb_off
    room2_btn_2_1.configure(command=lambda btn=room2_btn_2_1: toggle_image(btn))
    room2_btn_2_1.pack(side="top", ipadx=5, ipady=5)
    room2_cbbox_2_1 = ttk.Combobox(room2_frame_2_1, font="Verdana 20 bold", width=5, justify="center", textvariable=room2_cbbox_2_1_str, state="readonly", values=("One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Eleven","Twelve"))
    room2_cbbox_2_1.pack(anchor="n", pady=10) 
    room2_cbbox_2_1.set("Five")
    room2_cbbox_2_1.bind('<<ComboboxSelected>>', room2_2_1)
    room2_img_2_1 = ttk.Label(room2_frame_2_1, image=living_room_on)
    room2_img_2_1.config(anchor='center')
    room2_img_2_1.pack( expand=True)
    room2_img_2_1.configure(background="white")
    room2_frame_2_1.grid(row=1,column=1,sticky="nsew", padx=5,pady=5)
    #row 1, col 2
    room2_cbbox_2_2_str = tk.StringVar()
    room2_frame_2_2 = tk.Frame(room2_frame, borderwidth=2, relief="solid", background="white")
    room2_btn_2_2 = tk.Button(room2_frame_2_2, image=bulb_off, bg="white", fg="white")
    room2_btn_2_2.current_image = bulb_off
    room2_btn_2_2.configure(command=lambda btn=room2_btn_2_2: toggle_image(btn))
    room2_btn_2_2.pack(side="top", ipadx=5, ipady=5)
    room2_cbbox_2_2 = ttk.Combobox(room2_frame_2_2, font="Verdana 20 bold", width=5, justify="center", textvariable=room2_cbbox_2_2_str, state="readonly", values=("One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Eleven","Twelve"))
    room2_cbbox_2_2.pack(anchor="n", pady=10) 
    room2_cbbox_2_2.set("Six")
    room2_cbbox_2_2.bind('<<ComboboxSelected>>', room2_2_2)
    room2_img_2_2 = ttk.Label(room2_frame_2_2, image=living_room_on)
    room2_img_2_2.config(anchor='center')
    room2_img_2_2.pack( expand=True)
    room2_img_2_2.configure(background="white")
    room2_frame_2_2.grid(row=1,column=2,sticky="nsew", padx=5,pady=5)

    #row 1, col 3
    room2_cbbox_2_3_str = tk.StringVar()
    room2_frame_2_3 = tk.Frame(room2_frame, borderwidth=2, relief="solid", background="white")
    room2_btn_2_3 = tk.Button(room2_frame_2_3, image=bulb_off, bg="white", fg="white")
    room2_btn_2_3.current_image = bulb_off
    room2_btn_2_3.configure(command=lambda btn=room2_btn_2_3: toggle_image(btn))
    room2_btn_2_3.pack(side="top", ipadx=5, ipady=5)
    room2_cbbox_2_3 = ttk.Combobox(room2_frame_2_3, font="Verdana 20 bold", width=5, justify="center", textvariable=room2_cbbox_2_3_str, state="readonly", values=("One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Eleven","Twelve"))
    room2_cbbox_2_3.pack(anchor="n", pady=10) 
    room2_cbbox_2_3.set("Seven")
    room2_cbbox_2_3.bind('<<ComboboxSelected>>', room2_2_3)
    room2_img_2_3 = ttk.Label(room2_frame_2_3, image=living_room_on)
    room2_img_2_3.config(anchor='center')
    room2_img_2_3.pack( expand=True)
    room2_img_2_3.configure(background="white")
    room2_frame_2_3.grid(row=1,column=3,sticky="nsew", padx=5,pady=5)

    #row 1, col 4
    room2_cbbox_2_4_str = tk.StringVar()
    room2_frame_2_4 = tk.Frame(room2_frame, borderwidth=2, relief="solid", background="white")
    room2_btn_2_4 = tk.Button(room2_frame_2_4, image=bulb_off, bg="white", fg="white")
    room2_btn_2_4.current_image = bulb_off
    room2_btn_2_4.configure(command=lambda btn=room2_btn_2_4: toggle_image(btn))
    room2_btn_2_4.pack(side="top", ipadx=5, ipady=5)
    room2_cbbox_2_4 = ttk.Combobox(room2_frame_2_4, font="Verdana 20 bold", width=5, justify="center", textvariable=room2_cbbox_2_4_str, state="readonly", values=("One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Eleven","Twelve"))
    room2_cbbox_2_4.pack(anchor="n", pady=10) 
    room2_cbbox_2_4.set("Eight")
    room2_cbbox_2_4.bind('<<ComboboxSelected>>', room2_2_4)
    room2_img_2_4 = ttk.Label(room2_frame_2_4, image=living_room_on)
    room2_img_2_4.config(anchor='center')
    room2_img_2_4.pack( expand=True)
    room2_img_2_4.configure(background="white")
    room2_frame_2_4.grid(row=1,column=4,sticky="nsew", padx=5,pady=5)

    current_number = 0

    # Function to update the number and print it to console
    def update_number(queue):
        if not queue.empty():
            current_number = queue.get()
            print(current_number)
        window.after(1000, update_number, queue)

    # Start the updates
    update_number(current_number)

    window.mainloop()
    print('exited.........')
if __name__ == '__main__':
    queue = queue
    mainx(queue)
    