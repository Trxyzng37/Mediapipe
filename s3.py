import multiprocessing
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image  
import csv
import copy
import math

import time
import cv2 as cv
import tensorflow as tf
import numpy as np
import mediapipe as mp
import paho.mqtt.client as mqtt


received_message = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
device_status = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
prev_device_status = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
prev_hand_gesture = [0,0,0,0,0,0,0,0]
rasp_status = 0
esp_status = 0
cur_frame = 0 #0=living 1=bedroom

def mainx(queue):
    cbbox_value = ("No use","Zero","One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Eleven")

    def toggle_image(button):
        global device_status
        global prev_device_status
        prev_device_status = device_status.copy()
        current_img = button.current_image
        btn_index = devices_btn.index(button)
        #if off then on
        if current_img in device_img_off:
            img_index = device_img_off.index(current_img)
            new_image = device_img_on[img_index]
            button.config(image=new_image)
            button.current_image = new_image
            #get the status of device
            device_status[btn_index+1] = 1 
        #if on then off
        if current_img in device_img_on:
            img_index = device_img_on.index(current_img)
            new_image = device_img_off[img_index]
            button.config(image=new_image)
            button.current_image = new_image 
            device_status[btn_index+1] = 0 
        print("................................................")
        print("\nBefore pressed button: \n" + str(prev_device_status)) 
        print("After pressed button: \n" + str(device_status)) 
        publish_message()

    def publish_message():
        global prev_device_status
        global device_status
        if str(prev_device_status) == str(device_status):
            print("Same status as before")
        else:
            msg = str(device_status[1])+str(device_status[2])+str(device_status[3])+str(device_status[4])+str(device_status[5])+str(device_status[6])+str(device_status[7])+str(device_status[8])
            mqtt_client.publish("rasp4_to_esp32", str(msg), qos=2, retain=False)
            prev_device_status = device_status.copy()
            print("Publish to mqtt: \n" + str(msg))
            print("...........................................\n")

    def switch_to_room1(room1_btn, room2_btn):
        room1_frame.tkraise()
        global cur_frame
        cur_frame = 0
        new_room1_btn_img = living_room_on
        room1_btn.config(image=new_room1_btn_img)
        room1_btn.current_image = new_room1_btn_img
        new_room2_btn_img = bedroom_off
        room2_btn.config(image=new_room2_btn_img)
        room2_btn.current_image = new_room2_btn_img
        
    def switch_to_room2(room1_btn, room2_btn):    
        room2_frame.tkraise()
        global cur_frame
        cur_frame = 1
        new_room1_btn_img = living_room_off
        room1_btn.config(image=new_room1_btn_img)
        room1_btn.current_image = new_room1_btn_img
        new_room2_btn_img = bedroom_on
        room2_btn.config(image=new_room2_btn_img)
        room2_btn.current_image = new_room2_btn_img


    #define the window
    window = tk.Tk()
    window.title("ELECTRONIC DEVICES CONTROL SYSTEM USING HAND GESTURE RECOGNITION")
    #window.resizable(False,False)
    window.config(bg="white")
    #print(str(screen_width)+"|"+str(screen_height))
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

    fan_off = Image.open("img/fan_off.png")
    fan_off = fan_off.resize((200,200), Image.LANCZOS)
    fan_off = ImageTk.PhotoImage(fan_off)

    fan_on = Image.open("img/fan_on.png")
    fan_on = fan_on.resize((200,200), Image.LANCZOS)
    fan_on = ImageTk.PhotoImage(fan_on)

    tv_off = Image.open("img/tv_off.png")
    tv_off = tv_off.resize((200,200), Image.LANCZOS)
    tv_off = ImageTk.PhotoImage(tv_off)

    tv_on = Image.open("img/tv_on.png")
    tv_on = tv_on.resize((200,200), Image.LANCZOS)
    tv_on = ImageTk.PhotoImage(tv_on)

    air_off = Image.open("img/air_off.png")
    air_off = air_off.resize((200,200), Image.LANCZOS)
    air_off = ImageTk.PhotoImage(air_off)

    air_on = Image.open("img/air_on.png")
    air_on = air_on.resize((200,200), Image.LANCZOS)
    air_on = ImageTk.PhotoImage(air_on)

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

    no_use = Image.open("img/no_use.png")
    no_use = no_use.resize((90,100), Image.LANCZOS)
    no_use = ImageTk.PhotoImage(no_use)
    ###################################################################################

    # create main frame for window
    choice_frame = tk.Frame(window)
    choice_frame.grid(row=0, column=0, sticky="nsew")
    no1_frame = tk.Frame(window)
    no1_frame.grid(row=0, column=0, sticky="nsew")
    choice_frame.tkraise()
    
    # create frame for room 1
    no2_frame = tk.Frame(window)
    no2_frame.grid(row=0, column=1, sticky="nsew")
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
    no1_frame.grid_columnconfigure(0, weight=1)
    no2_frame.grid_columnconfigure(0, weight=1)

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

#no status
    no_check = tk.StringVar()
    no_check = "Host block = OFFLINE\nClient block = OFFLINE"
    no1_label = ttk.Label(no1_frame, text="", font=("Arial", 40), anchor="center", justify="center")
    no1_label.pack(fill=tk.BOTH, expand=True)
    no1_label.configure(background="red")
    no12_label = ttk.Label(no2_frame, text="\nSystem internet connection status\n", font=("Arial", 40), anchor="center", justify="center")
    no12_label.pack(fill=tk.X)
    no12_label.configure(background="red")
    no2_label = ttk.Label(no2_frame, text=no_check, font=("Arial", 40), anchor="center", justify="left")
    no2_label.pack(fill=tk.BOTH, expand=True)
    no2_label.configure(background="red")
    #room1 frame###############################
    # Merge cells in the device frame and add text
    label = ttk.Label(room1_frame, text="HOẶC CHÍ TRUNG - NGUYỄN GIA HƯNG\n ELECTRONIC DEVICES CONTROL SYSTEM USING HAND GESTURE RECOGNITION\nHo Chi Minh City University of Technology and Education", font=("Arial", 8), anchor="center", justify="center")
    label.grid(row=0, column=1, ipadx=0, ipady=10, padx=5, pady=5, sticky="nsew", columnspan=4)
    label.configure(background="white")

    def room1_1_1(event):
        selected_value = room1_cbbox_1_1.get()
        if selected_value == 'Zero':
            image_path = f"img/h0.jpg"
        if selected_value == 'One':
            image_path = f"img/h1.jpg"
        elif selected_value == 'Two':
            image_path = 'img/h2.jpg'
        elif selected_value == 'Three':
            image_path = 'img/h3.jpg'
        elif selected_value == 'Four':
            image_path = 'img/h4.jpg'
        elif selected_value == 'Five':
            image_path = 'img/h5.jpg'
        elif selected_value == 'Six':
            image_path = 'img/h6.jpg'
        elif selected_value == 'Seven':
            image_path = 'img/h7.jpg'
        elif selected_value == 'Eight':
            image_path = 'img/h8.jpg'
        if selected_value == 'Nine':
            image_path = f"img/h9.jpg"
        if selected_value == 'Ten':
            image_path = f"img/h10.jpg"
        if selected_value == 'Eleven':
            image_path = f"img/h11.jpg"
        if selected_value == 'No use':        
            image_path = f"img/no_use.png"

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        room1_img_1_1.configure(image=current_image)
        room1_img_1_1.image = current_image
        print(selected_value)

    def room1_1_2(event):
        selected_value = room1_cbbox_1_2.get()
        if selected_value == 'Zero':
            image_path = f"img/h0.jpg"
        if selected_value == 'One':
            image_path = f"img/h1.jpg"
        elif selected_value == 'Two':
            image_path = 'img/h2.jpg'
        elif selected_value == 'Three':
            image_path = 'img/h3.jpg'
        elif selected_value == 'Four':
            image_path = 'img/h4.jpg'
        elif selected_value == 'Five':
            image_path = 'img/h5.jpg'
        elif selected_value == 'Six':
            image_path = 'img/h6.jpg'
        elif selected_value == 'Seven':
            image_path = 'img/h7.jpg'
        elif selected_value == 'Eight':
            image_path = 'img/h8.jpg'
        if selected_value == 'Nine':
            image_path = f"img/h9.jpg"
        if selected_value == 'Ten':
            image_path = f"img/h10.jpg"
        if selected_value == 'Eleven':
            image_path = f"img/h11.jpg"
        if selected_value == 'No use':        
            image_path = f"img/no_use.png"

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        room1_img_1_2.configure(image=current_image)
        room1_img_1_2.image = current_image
        print(selected_value)

    def room1_1_3(event):
        selected_value = room1_cbbox_1_3.get()
        if selected_value == 'Zero':
            image_path = f"img/h0.jpg"
        if selected_value == 'One':
            image_path = f"img/h1.jpg"
        elif selected_value == 'Two':
            image_path = 'img/h2.jpg'
        elif selected_value == 'Three':
            image_path = 'img/h3.jpg'
        elif selected_value == 'Four':
            image_path = 'img/h4.jpg'
        elif selected_value == 'Five':
            image_path = 'img/h5.jpg'
        elif selected_value == 'Six':
            image_path = 'img/h6.jpg'
        elif selected_value == 'Seven':
            image_path = 'img/h7.jpg'
        elif selected_value == 'Eight':
            image_path = 'img/h8.jpg'
        if selected_value == 'Nine':
            image_path = f"img/h9.jpg"
        if selected_value == 'Ten':
            image_path = f"img/h10.jpg"
        if selected_value == 'Eleven':
            image_path = f"img/h11.jpg"
        if selected_value == 'No use':        
            image_path = f"img/no_use.png"

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        room1_img_1_3.configure(image=current_image)
        room1_img_1_3.image = current_image
        print(selected_value)

    def room1_1_4(event):
        selected_value = room1_cbbox_1_4.get()
        if selected_value == 'Zero':
            image_path = f"img/h0.jpg"
        if selected_value == 'One':
            image_path = f"img/h1.jpg"
        elif selected_value == 'Two':
            image_path = 'img/h2.jpg'
        elif selected_value == 'Three':
            image_path = 'img/h3.jpg'
        elif selected_value == 'Four':
            image_path = 'img/h4.jpg'
        elif selected_value == 'Five':
            image_path = 'img/h5.jpg'
        elif selected_value == 'Six':
            image_path = 'img/h6.jpg'
        elif selected_value == 'Seven':
            image_path = 'img/h7.jpg'
        elif selected_value == 'Eight':
            image_path = 'img/h8.jpg'
        if selected_value == 'Nine':
            image_path = f"img/h9.jpg"
        if selected_value == 'Ten':
            image_path = f"img/h10.jpg"
        if selected_value == 'Eleven':
            image_path = f"img/h11.jpg"
        if selected_value == 'No use':        
            image_path = f"img/no_use.png"

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        room1_img_1_4.configure(image=current_image)
        room1_img_1_4.image = current_image
        print(selected_value)

    def room2_2_1(event):
        selected_value = room2_cbbox_2_1.get()
        if selected_value == 'Zero':
            image_path = f"img/h0.jpg"
        if selected_value == 'One':
            image_path = f"img/h1.jpg"
        elif selected_value == 'Two':
            image_path = 'img/h2.jpg'
        elif selected_value == 'Three':
            image_path = 'img/h3.jpg'
        elif selected_value == 'Four':
            image_path = 'img/h4.jpg'
        elif selected_value == 'Five':
            image_path = 'img/h5.jpg'
        elif selected_value == 'Six':
            image_path = 'img/h6.jpg'
        elif selected_value == 'Seven':
            image_path = 'img/h7.jpg'
        elif selected_value == 'Eight':
            image_path = 'img/h8.jpg'
        if selected_value == 'Nine':
            image_path = f"img/h9.jpg"
        if selected_value == 'Ten':
            image_path = f"img/h10.jpg"
        if selected_value == 'Eleven':
            image_path = f"img/h11.jpg"
        if selected_value == 'No use':        
            image_path = f"img/no_use.png"

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        room2_img_2_1.configure(image=current_image)
        room2_img_2_1.image = current_image
        print(selected_value)

    def room2_2_2(event):
        selected_value = room2_cbbox_2_2.get()
        if selected_value == 'Zero':
            image_path = f"img/h0.jpg"
        if selected_value == 'One':
            image_path = f"img/h1.jpg"
        elif selected_value == 'Two':
            image_path = 'img/h2.jpg'
        elif selected_value == 'Three':
            image_path = 'img/h3.jpg'
        elif selected_value == 'Four':
            image_path = 'img/h4.jpg'
        elif selected_value == 'Five':
            image_path = 'img/h5.jpg'
        elif selected_value == 'Six':
            image_path = 'img/h6.jpg'
        elif selected_value == 'Seven':
            image_path = 'img/h7.jpg'
        elif selected_value == 'Eight':
            image_path = 'img/h8.jpg'
        if selected_value == 'Nine':
            image_path = f"img/h9.jpg"
        if selected_value == 'Ten':
            image_path = f"img/h10.jpg"
        if selected_value == 'Eleven':
            image_path = f"img/h11.jpg"
        if selected_value == 'No use':        
            image_path = f"img/no_use.png"

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        room2_img_2_2.configure(image=current_image)
        room2_img_2_2.image = current_image
        print(selected_value)

    def room2_2_3(event):
        selected_value = room2_cbbox_2_3.get()
        if selected_value == 'Zero':
            image_path = f"img/h0.jpg"
        if selected_value == 'One':
            image_path = f"img/h1.jpg"
        elif selected_value == 'Two':
            image_path = 'img/h2.jpg'
        elif selected_value == 'Three':
            image_path = 'img/h3.jpg'
        elif selected_value == 'Four':
            image_path = 'img/h4.jpg'
        elif selected_value == 'Five':
            image_path = 'img/h5.jpg'
        elif selected_value == 'Six':
            image_path = 'img/h6.jpg'
        elif selected_value == 'Seven':
            image_path = 'img/h7.jpg'
        elif selected_value == 'Eight':
            image_path = 'img/h8.jpg'
        if selected_value == 'Nine':
            image_path = f"img/h9.jpg"
        if selected_value == 'Ten':
            image_path = f"img/h10.jpg"
        if selected_value == 'Eleven':
            image_path = f"img/h11.jpg"
        if selected_value == 'No use':        
            image_path = f"img/no_use.png"

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        room2_img_2_3.configure(image=current_image)
        room2_img_2_3.image = current_image
        print(selected_value)

    def room2_2_4(event):
        selected_value = room2_cbbox_2_4.get()
        if selected_value == 'Zero':
            image_path = f"img/h0.jpg"
        if selected_value == 'One':
            image_path = f"img/h1.jpg"
        elif selected_value == 'Two':
            image_path = 'img/h2.jpg'
        elif selected_value == 'Three':
            image_path = 'img/h3.jpg'
        elif selected_value == 'Four':
            image_path = 'img/h4.jpg'
        elif selected_value == 'Five':
            image_path = 'img/h5.jpg'
        elif selected_value == 'Six':
            image_path = 'img/h6.jpg'
        elif selected_value == 'Seven':
            image_path = 'img/h7.jpg'
        elif selected_value == 'Eight':
            image_path = 'img/h8.jpg'
        if selected_value == 'Nine':
            image_path = f"img/h9.jpg"
        if selected_value == 'Ten':
            image_path = f"img/h10.jpg"
        if selected_value == 'Eleven':
            image_path = f"img/h11.jpg"
        if selected_value == 'No use':        
            image_path = f"img/no_use.png"

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        room2_img_2_4.configure(image=current_image)
        room2_img_2_4.image = current_image
        print(selected_value)

###room 1
    #row 1, col 1
    room1_cbbox_1_1_str = tk.StringVar()
    room1_frame_1_1 = tk.Frame(room1_frame, borderwidth=2, relief="solid", background="white")
    room1_btn_1_1 = tk.Button(room1_frame_1_1, image=bulb_off, bg="white", fg="white")
    room1_btn_1_1.current_image = bulb_off
    room1_btn_1_1.configure(command=lambda btn=room1_btn_1_1: toggle_image(btn))
    room1_btn_1_1.pack(side="top", ipadx=5, ipady=5)
    room1_cbbox_1_1 = ttk.Combobox(room1_frame_1_1, font="Verdana 20 bold", width=8, justify="center", textvariable=room1_cbbox_1_1_str, state="readonly", values=cbbox_value)
    room1_cbbox_1_1.pack(anchor="n", pady=10) 
    room1_cbbox_1_1.set("No use")
    room1_cbbox_1_1.bind('<<ComboboxSelected>>', room1_1_1)
    room1_img_1_1 = ttk.Label(room1_frame_1_1, image=no_use)
    room1_img_1_1.config(anchor='center')
    room1_img_1_1.pack( expand=True)
    room1_img_1_1.configure(background="white")
    room1_frame_1_1.grid(row=1,column=1,sticky="nsew", padx=5,pady=5)
    #row 1, col 2
    room1_cbbox_1_2_str = tk.StringVar()
    room1_frame_1_2 = tk.Frame(room1_frame, borderwidth=2, relief="solid", background="white")
    room1_btn_1_2 = tk.Button(room1_frame_1_2, image=fan_off, bg="white", fg="white")
    room1_btn_1_2.current_image = fan_off
    room1_btn_1_2.configure(command=lambda btn=room1_btn_1_2: toggle_image(btn))
    room1_btn_1_2.pack(side="top", ipadx=5, ipady=5)
    room1_cbbox_1_2 = ttk.Combobox(room1_frame_1_2, font="Verdana 20 bold", width=8, justify="center", textvariable=room1_cbbox_1_2_str, state="readonly", values=cbbox_value)
    room1_cbbox_1_2.pack(anchor="n", pady=10) 
    room1_cbbox_1_2.set("No use")
    room1_cbbox_1_2.bind('<<ComboboxSelected>>', room1_1_2)
    room1_img_1_2 = ttk.Label(room1_frame_1_2, image=no_use)
    room1_img_1_2.config(anchor='center')
    room1_img_1_2.pack( expand=True)
    room1_img_1_2.configure(background="white")
    room1_frame_1_2.grid(row=1,column=2,sticky="nsew", padx=5,pady=5)

    #row 1, col 3
    room1_cbbox_1_3_str = tk.StringVar()
    room1_frame_1_3 = tk.Frame(room1_frame, borderwidth=2, relief="solid", background="white")
    room1_btn_1_3 = tk.Button(room1_frame_1_3, image=tv_off, bg="white", fg="white")
    room1_btn_1_3.current_image = tv_off
    room1_btn_1_3.configure(command=lambda btn=room1_btn_1_3: toggle_image(btn))
    room1_btn_1_3.pack(side="top", ipadx=5, ipady=5)
    room1_cbbox_1_3 = ttk.Combobox(room1_frame_1_3, font="Verdana 20 bold", width=8, justify="center", textvariable=room1_cbbox_1_3_str, state="readonly", values=cbbox_value)
    room1_cbbox_1_3.pack(anchor="n", pady=10) 
    room1_cbbox_1_3.set("No use")
    room1_cbbox_1_3.bind('<<ComboboxSelected>>', room1_1_3)
    room1_img_1_3 = ttk.Label(room1_frame_1_3, image=no_use)
    room1_img_1_3.config(anchor='center')
    room1_img_1_3.pack( expand=True)
    room1_img_1_3.configure(background="white")
    room1_frame_1_3.grid(row=1,column=3,sticky="nsew", padx=5,pady=5)
    #row 1, col 4
    room1_cbbox_1_4_str = tk.StringVar()
    room1_frame_1_4 = tk.Frame(room1_frame, borderwidth=2, relief="solid", background="white")
    room1_btn_1_4 = tk.Button(room1_frame_1_4, image=air_off, bg="white", fg="white")
    room1_btn_1_4.current_image = air_off
    room1_btn_1_4.configure(command=lambda btn=room1_btn_1_4: toggle_image(btn))
    room1_btn_1_4.pack(side="top", ipadx=5, ipady=5)
    room1_cbbox_1_4 = ttk.Combobox(room1_frame_1_4, font="Verdana 20 bold", width=8, justify="center", textvariable=room1_cbbox_1_4_str, state="readonly", values=cbbox_value)
    room1_cbbox_1_4.pack(anchor="n", pady=10) 
    room1_cbbox_1_4.set("No use")
    room1_cbbox_1_4.bind('<<ComboboxSelected>>', room1_1_4)
    room1_img_1_4 = ttk.Label(room1_frame_1_4, image=no_use)
    room1_img_1_4.config(anchor='center')
    room1_img_1_4.pack( expand=True)
    room1_img_1_4.configure(background="white")
    room1_frame_1_4.grid(row=1,column=4,sticky="nsew", padx=5,pady=5)


    ####################################room2 
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
    room2_cbbox_2_1 = ttk.Combobox(room2_frame_2_1, font="Verdana 20 bold", width=8, justify="center", textvariable=room2_cbbox_2_1_str, state="readonly", values=cbbox_value)
    room2_cbbox_2_1.pack(anchor="n", pady=10) 
    room2_cbbox_2_1.set("No use")
    room2_cbbox_2_1.bind('<<ComboboxSelected>>', room2_2_1)
    room2_img_2_1 = ttk.Label(room2_frame_2_1, image=no_use)
    room2_img_2_1.config(anchor='center')
    room2_img_2_1.pack( expand=True)
    room2_img_2_1.configure(background="white")
    room2_frame_2_1.grid(row=1,column=1,sticky="nsew", padx=5,pady=5)
    #row 1, col 2
    room2_cbbox_2_2_str = tk.StringVar()
    room2_frame_2_2 = tk.Frame(room2_frame, borderwidth=2, relief="solid", background="white")
    room2_btn_2_2 = tk.Button(room2_frame_2_2, image=fan_off, bg="white", fg="white")
    room2_btn_2_2.current_image = fan_off
    room2_btn_2_2.configure(command=lambda btn=room2_btn_2_2: toggle_image(btn))
    room2_btn_2_2.pack(side="top", ipadx=5, ipady=5)
    room2_cbbox_2_2 = ttk.Combobox(room2_frame_2_2, font="Verdana 20 bold", width=8, justify="center", textvariable=room2_cbbox_2_2_str, state="readonly", values=cbbox_value)
    room2_cbbox_2_2.pack(anchor="n", pady=10) 
    room2_cbbox_2_2.set("No use")
    room2_cbbox_2_2.bind('<<ComboboxSelected>>', room2_2_2)
    room2_img_2_2 = ttk.Label(room2_frame_2_2, image=no_use)
    room2_img_2_2.config(anchor='center')
    room2_img_2_2.pack( expand=True)
    room2_img_2_2.configure(background="white")
    room2_frame_2_2.grid(row=1,column=2,sticky="nsew", padx=5,pady=5)

    #row 1, col 3
    room2_cbbox_2_3_str = tk.StringVar()
    room2_frame_2_3 = tk.Frame(room2_frame, borderwidth=2, relief="solid", background="white")
    room2_btn_2_3 = tk.Button(room2_frame_2_3, image=tv_off, bg="white", fg="white")
    room2_btn_2_3.current_image = tv_off
    room2_btn_2_3.configure(command=lambda btn=room2_btn_2_3: toggle_image(btn))
    room2_btn_2_3.pack(side="top", ipadx=5, ipady=5)
    room2_cbbox_2_3 = ttk.Combobox(room2_frame_2_3, font="Verdana 20 bold", width=8, justify="center", textvariable=room2_cbbox_2_3_str, state="readonly", values=cbbox_value)
    room2_cbbox_2_3.pack(anchor="n", pady=10) 
    room2_cbbox_2_3.set("No use")
    room2_cbbox_2_3.bind('<<ComboboxSelected>>', room2_2_3)
    room2_img_2_3 = ttk.Label(room2_frame_2_3, image=no_use)
    room2_img_2_3.config(anchor='center')
    room2_img_2_3.pack( expand=True)
    room2_img_2_3.configure(background="white")
    room2_frame_2_3.grid(row=1,column=3,sticky="nsew", padx=5,pady=5)

    #row 1, col 4
    room2_cbbox_2_4_str = tk.StringVar()
    room2_frame_2_4 = tk.Frame(room2_frame, borderwidth=2, relief="solid", background="white")
    room2_btn_2_4 = tk.Button(room2_frame_2_4, image=air_off, bg="white", fg="white")
    room2_btn_2_4.current_image = air_off
    room2_btn_2_4.configure(command=lambda btn=room2_btn_2_4: toggle_image(btn))
    room2_btn_2_4.pack(side="top", ipadx=5, ipady=5)
    room2_cbbox_2_4 = ttk.Combobox(room2_frame_2_4, font="Verdana 20 bold", width=8, justify="center", textvariable=room2_cbbox_2_4_str, state="readonly", values=cbbox_value)
    room2_cbbox_2_4.pack(anchor="n", pady=10) 
    room2_cbbox_2_4.set("No use")
    room2_cbbox_2_4.bind('<<ComboboxSelected>>', room2_2_4)
    room2_img_2_4 = ttk.Label(room2_frame_2_4, image=no_use)
    room2_img_2_4.config(anchor='center')
    room2_img_2_4.pack( expand=True)
    room2_img_2_4.configure(background="white")
    room2_frame_2_4.grid(row=1,column=4,sticky="nsew", padx=5,pady=5)
    
    #define variables
    comboboxes = (room1_cbbox_1_1, room1_cbbox_1_2, room1_cbbox_1_3, room1_cbbox_1_4, room2_cbbox_2_1, room2_cbbox_2_2, room2_cbbox_2_3, room2_cbbox_2_4)
    devices_btn = (room1_btn_1_1, room1_btn_1_2, room1_btn_1_3, room1_btn_1_4, room2_btn_2_1, room2_btn_2_2, room2_btn_2_3, room2_btn_2_4)
    device_img_off = (bulb_off, fan_off, tv_off, air_off)
    device_img_on = (bulb_on, fan_on, tv_on, air_on)

    # Function to update the number and print it to console
    def receive_hand_gesture(queue, comboboxes, devices_btn, device_img_off, device_img_on):
        if not queue.empty():
            current_gesture = queue.get()
            #receive value from 0 to 11
            mapped_gesture = {
                0: "Zero",
                1: "One",
                2: "Two",
                3: "Four",
                4: "Five",
                5: "Three",
                6: "Six",
                7: "Seven",
                8: "Eight",
                9: "Nine",
                10: "Ten",
                11: "Eleven"
            }

            current_gesture = mapped_gesture[current_gesture]
            print("get from queue: " + str(current_gesture))
            for cbbox in comboboxes:
                #check if any combobox has the same gesture as received value
                if cbbox.get() == current_gesture:
                    #get which combobox is have that gesture value
                    device_index = comboboxes.index(cbbox)
                    #get the current image corresponding to the device status
                    current_img = devices_btn[device_index].current_image
                    #if off then on
                    if current_img in device_img_off:
                        #find index
                        img_index = device_img_off.index(current_img)
                        new_image = device_img_on[img_index]
                        devices_btn[device_index].config(image=new_image)
                        devices_btn[device_index].current_image = new_image
                        #get the status of device
                        device_status[device_index+1] = 1 
                    #if on then off
                    if current_img in device_img_on:
                        img_index = device_img_on.index(current_img)
                        new_image = device_img_off[img_index]
                        devices_btn[device_index].config(image=new_image)
                        devices_btn[device_index].current_image = new_image 
                        device_status[device_index+1] = 0 
            print("After detect gesture: \n" + str(device_status))   
            publish_message()
        window.after(1, receive_hand_gesture, queue, comboboxes, devices_btn, device_img_off, device_img_on)

    def process_received_message():
        global received_message
        nonlocal devices_btn
        print("Message for process: \n"+ str(received_message) + "\n")
        
        for key, value in received_message.items():
            current_img = devices_btn[key-1].current_image
            if current_img in device_img_off:
                #find index
                img_index = device_img_off.index(current_img)
                if value == 0:
                    new_image = device_img_off[img_index]
                if value == 1:
                    new_image = device_img_on[img_index]
            if current_img in device_img_on:
                img_index = device_img_on.index(current_img)
                if value == 0:
                    new_image = device_img_off[img_index]
                if value == 1:
                    new_image = device_img_on[img_index]                
            devices_btn[key-1].config(image=new_image)   
            devices_btn[key-1].current_image = new_image
    
    # Start the updates
    receive_hand_gesture(queue, comboboxes, devices_btn, device_img_off, device_img_on)


    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connection successful")
            mqtt_client.publish("trxyzng_r_status", "ron", qos=2, retain=True)
            room1_frame.tkraise()
            choice_frame.tkraise()
            global rasp_status
            rasp_status = 1
        else:
            print("Connection failed")

    def on_disconnect(client, userdata, rc):
        print("Disconnected from MQTT broker.\n")
        print("Atempt to reconnect................")
        no1_frame.tkraise()
        no2_frame.tkraise()
        global rasp_status
        rasp_status = 0

    def on_message(client, userdata, message):
        global received_message
        global prev_device_status
        global device_status
        global esp_status
        global rasp_status
        msg = str(message.payload.decode("utf-8"))
        if len(msg) == 8:
            #received_message = eval(msg)
            received_message[1] = int(msg[0])
            received_message[2] = int(msg[1])
            received_message[3] = int(msg[2])
            received_message[4] = int(msg[3])
            received_message[5] = int(msg[4])
            received_message[6] = int(msg[5])
            received_message[7] = int(msg[6])
            received_message[8] = int(msg[7])
            print("Get from mqtt: \n" + msg)
            prev_device_status = device_status.copy()
            device_status = received_message.copy()
            process_received_message()
        else:
            if msg == "0":
                prev_hand_gesture[0] = room1_cbbox_1_1.get()
                prev_hand_gesture[1] = room1_cbbox_1_2.get()
                prev_hand_gesture[2] = room1_cbbox_1_3.get()
                prev_hand_gesture[3] = room1_cbbox_1_4.get()
                prev_hand_gesture[4] = room2_cbbox_2_1.get()
                prev_hand_gesture[5] = room2_cbbox_2_2.get()
                prev_hand_gesture[6] = room2_cbbox_2_3.get()
                prev_hand_gesture[7] = room2_cbbox_2_4.get()
                room1_cbbox_1_1.set("No use")
                room1_cbbox_1_2.set("No use")
                room1_cbbox_1_3.set("No use")
                room1_cbbox_1_4.set("No use")
                room2_cbbox_2_1.set("No use")
                room2_cbbox_2_2.set("No use")
                room2_cbbox_2_3.set("No use")
                room2_cbbox_2_4.set("No use")
                room1_img_1_1.configure(image=no_use)
                room1_img_1_1.image = no_use
                room1_img_1_2.configure(image=no_use)
                room1_img_1_2.image = no_use
                room1_img_1_3.configure(image=no_use)
                room1_img_1_3.image = no_use
                room1_img_1_4.configure(image=no_use)
                room1_img_1_4.image = no_use
                room2_img_2_1.configure(image=no_use)
                room2_img_2_1.image = no_use
                room2_img_2_2.configure(image=no_use)
                room2_img_2_2.image = no_use
                room2_img_2_3.configure(image=no_use)
                room2_img_2_3.image = no_use
                room2_img_2_4.configure(image=no_use)
                room2_img_2_4.image = no_use
                pre = ""
                for i in range(len(prev_hand_gesture)):
                    pre = pre + prev_hand_gesture[i]
                print("Previous gesture: "+pre+"\n")
            elif msg == "1":
                if room1_cbbox_1_1.get() != "No use":
                    pass
                else:
                    room1_cbbox_1_1.set(prev_hand_gesture[0])
                    change_hand(room1_cbbox_1_1, room1_img_1_1)
                if room1_cbbox_1_2.get() != "No use":
                    pass
                else:
                    room1_cbbox_1_2.set(prev_hand_gesture[1])
                    change_hand(room1_cbbox_1_2, room1_img_1_2) 
                if room1_cbbox_1_3.get() != "No use":
                    pass
                else:
                    room1_cbbox_1_3.set(prev_hand_gesture[2])
                    change_hand(room1_cbbox_1_3, room1_img_1_3)  
                if room1_cbbox_1_4.get() != "No use":
                    pass
                else:
                    room1_cbbox_1_4.set(prev_hand_gesture[3])
                    change_hand(room1_cbbox_1_4, room1_img_1_4)             
                if room2_cbbox_2_1.get() != "No use":
                    pass
                else:
                    room2_cbbox_2_1.set(prev_hand_gesture[4])
                    change_hand(room2_cbbox_2_1, room2_img_2_1)
                if room2_cbbox_2_2.get() != "No use":
                    pass
                else:
                    room2_cbbox_2_2.set(prev_hand_gesture[5])
                    change_hand(room2_cbbox_2_2, room2_img_2_2)
                if room2_cbbox_2_3.get() != "No use":
                    pass
                else:
                    room2_cbbox_2_3.set(prev_hand_gesture[6])
                    change_hand(room2_cbbox_2_3, room2_img_2_3)  
                if room2_cbbox_2_4.get() != "No use":
                    pass
                else:
                    room2_cbbox_2_4.set(prev_hand_gesture[7])
                    change_hand(room2_cbbox_2_4, room2_img_2_4)              

            elif msg == "on":
                # choice_frame.tkraise()
                # room1_frame.tkraise()
                esp_status = 1
            elif msg == "off":
                # no1_frame.tkraise()
                # no2_frame.tkraise()
                esp_status = 0
            elif msg == "ron":
                rasp_status = 1                

    def change_hand(ccbox, img):
        image_path = f"img/no_use.png"
        selected_value = ccbox.get()
        if selected_value == 'Zero':
            image_path = f"img/h0.jpg"
        if selected_value == 'One':
            image_path = f"img/h1.jpg"
        elif selected_value == 'Two':
            image_path = 'img/h2.jpg'
        elif selected_value == 'Three':
            image_path = 'img/h3.jpg'
        elif selected_value == 'Four':
            image_path = 'img/h4.jpg'
        elif selected_value == 'Five':
            image_path = 'img/h5.jpg'
        elif selected_value == 'Six':
            image_path = 'img/h6.jpg'
        elif selected_value == 'Seven':
            image_path = 'img/h7.jpg'
        elif selected_value == 'Eight':
            image_path = 'img/h8.jpg'
        if selected_value == 'Nine':
            image_path = f"img/h9.jpg"
        if selected_value == 'Ten':
            image_path = f"img/h10.jpg"
        if selected_value == 'Eleven':
            image_path = f"img/h11.jpg"
        if selected_value == 'No use':        
            image_path = f"img/no_use.png"

        current_image = Image.open(image_path)
        current_image = current_image.resize((90,100), Image.LANCZOS)
        current_image = ImageTk.PhotoImage(current_image)
        img.configure(image=current_image)
        img.image = current_image
        print(selected_value)


    def connect_to_mqtt():
        broker_address = "broker.hivemq.com"         #address of cloud mqtt server 
        port = 1883                                  #port to connect to mqtt server
        client = mqtt.Client(client_id="hoacchitrung_nguyengiahung_computer", clean_session=False, userdata=None, protocol=mqtt.MQTTv311, transport="tcp") #create new client
        print("Connecting to broker...")          #print to console
        client.will_set("trxyzng_r_status", "roff", 2, True)
        client.connect(broker_address, port, 5)   #connect to broker with keep alive time = 5s
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.subscribe("esp32_to_rasp4", qos=2)
        client.subscribe("trxyzng_status", qos=2)
        client.subscribe("trxyzng_r_status", qos=2)
        client.on_message = on_message
        client.loop_start()
        return client
    

    mqtt_client = connect_to_mqtt()    

    def device_disconnected():
        global rasp_status
        global esp_status
        global no_check
        if rasp_status == 1 and esp_status == 1:
            global cur_frame
            if cur_frame == 0:
                room1_frame.tkraise()
                choice_frame.tkraise()
            else:
                room2_frame.tkraise()
                choice_frame.tkraise()
        else:
            no1_frame.tkraise()
            no2_frame.tkraise()
        print(str(rasp_status) + "|" + str(esp_status) + "\n")
        r = "ONLINE" if rasp_status == 1 else "OFFLINE"
        e = "ONLINE" if esp_status == 1 else "OFFLINE"
        no2_label.config(text=f"Host block = {r}\nClient block = {e}") 
        window.after(1000, device_disconnected)
    

    device_disconnected()

    window.mainloop()
    print('exited.........')



##### hand gesture detection
def classifier_gesture(queue):
    # define some default variables
    cap = cv.VideoCapture(0)
    prev_time = 0
    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    with open('label.csv', encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [row[0] for row in keypoint_classifier_labels]

    prev_occurence = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0
    }
    frame_count = 0
    current_frame = None
    delay_time = 4
    
    while True:
        key = cv.waitKey(1)
        ret, image = cap.read()
        frame_count += 1
        
        curr_time = cv.getTickCount()
        time_taken = (curr_time - prev_time) / cv.getTickFrequency()
        fps = math.ceil(1 / time_taken)
        prev_time = curr_time

        if frame_count % 5 == 0:
            current_frame = image
            current_frame = cv.flip(current_frame, 1)
            results = hands.process(current_frame)
            if results.multi_hand_landmarks is not None:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    bounding_box = calc_bounding_box(current_frame, hand_landmarks)
                    landmark_list = calc_landmark_list(current_frame, hand_landmarks)
                    normalized_processed_landmark_list = calc_normalized_processed_landmark_list(landmark_list)
                    hand_sign_id = key_point_classifier(normalized_processed_landmark_list)
                    if hand_sign_id is None:
                        pass
                    else:
                        if prev_occurence[hand_sign_id] == 0:
                            prev_occurence[hand_sign_id] = int(time.time())
                            queue.put(hand_sign_id)
                            print("put to queue: "+str(hand_sign_id))
                        else:
                            if int(time.time()) - prev_occurence[hand_sign_id] >= delay_time: 
                                queue.put(hand_sign_id)
                                print("put to queue: "+str(hand_sign_id))
                                prev_occurence[hand_sign_id] = int(time.time())
                            else:
                                pass

                    current_frame = draw_bounding_box(current_frame, bounding_box)
                    current_frame = draw_landmarks(current_frame, landmark_list)
                    current_frame = draw_info_text(current_frame, bounding_box, handedness, keypoint_classifier_labels, hand_sign_id)
            current_frame = draw_fps(current_frame, fps)
            cv.imshow('Hand Gesture Recognition', current_frame)
        else:
            pass
        if key == 27:  # ESC
            break

        if not ret:
            break


    cap.release()
    cv.destroyAllWindows()
    print("Close hand gesture.......")



# calculate the bounding box for hand on image
def calc_bounding_box(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
    landmark_array = np.empty((0, 2), int)
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_point = [np.array((landmark_x, landmark_y))]
        landmark_array = np.append(landmark_array, landmark_point, axis=0)
    x, y, w, h = cv.boundingRect(landmark_array)
    return [x, y, x + w, y + h]


# process the result key point value from medapipe in range (0,1) to value base on image size
def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
    landmark_point = []
    for landmark in landmarks.landmark:
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_point.append([landmark_x, landmark_y])
    # return a list with each element is a list contain x,y value    
    return landmark_point

# process the key point value base on image size, and normalize it into value in range (-1,1) 
def calc_normalized_processed_landmark_list(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)
    # Convert to relative coordinates base on the wrist position
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]
        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y
    # Convert a list of list into a single list
    # temp_landmark_list = list(
    #     itertools.chain.from_iterable(temp_landmark_list))
    temp_landmark_list = sum(temp_landmark_list, [])
    #print(temp_landmark_list)
    #for each value in the list, find the absolute value of it, then find the maximum value in the list
    max_value = max(list(map(abs, temp_landmark_list)))
    def normalize_(n):
        return n / max_value
    # for each value in list, divide it with the maximum value in the list
    temp_landmark_list = list(map(normalize_, temp_landmark_list))
    return temp_landmark_list

# from the result from mediapipe, run it through the classifier to detect which hand gesture is it
def key_point_classifier(landmark_list, model_path='keypoint_classifier.tflite', num_threads=1):
    interpreter = tf.lite.Interpreter(model_path = model_path, num_threads=num_threads)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    input_details_tensor_index = input_details[0]['index']
    interpreter.set_tensor(input_details_tensor_index, np.array([landmark_list], dtype=np.float32))
    interpreter.invoke()
    output_details_tensor_index = output_details[0]['index']
    result = interpreter.get_tensor(output_details_tensor_index)
    # find the maximum probability class
    max_result_probability = np.max(np.squeeze(result))
    #print(max_result_probability)
    if max_result_probability > 0.9:
        result_index = np.argmax(np.squeeze(result))
    # if all probability for classes is less than 0.9, output None
    else:
        result_index = None
    return result_index

# draw the landmark
def draw_landmarks(image, landmark_point):
    if len(landmark_point) > 0:
        # Thumb

        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                (255, 255, 255), 1)

        # Index finger

        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                (255, 255, 255), 1)

        # Middle finger

        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                (255, 255, 255), 1)

        # Ring finger

        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                (255, 255, 255), 1)

        # Little finger

        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                (255, 255, 255), 1)

        # Palm

        cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                (255, 255, 255), 1)

    # Key Points
    for index, landmark in enumerate(landmark_point):
        if index == 0:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 1:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 2:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 3:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 4:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 5:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 6:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 7:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 8:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 9:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 10:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 11:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 12:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 13:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 14:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 15:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 16:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 17:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 18:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 19:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 20:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
    return image

# draw the bounding box
def draw_bounding_box(image, bounding_box):
    cv.rectangle(image, (bounding_box[0], bounding_box[1]), (bounding_box[2], bounding_box[3]),(0, 0, 0), 1)
    return image

# draw hand gesture result
def draw_info_text(image, bounding_box, handedness, keypoint_classifier_labels, hand_sign_id):
    cv.rectangle(image, (bounding_box[0], bounding_box[1]), (bounding_box[2], bounding_box[1] - 22), (0, 0, 0), -1)
    info_text = handedness.classification[0].label[0:]
    if hand_sign_id == None:
        info_text = info_text + ':' + "No result"
    else:
        info_text = info_text + ':' + keypoint_classifier_labels[hand_sign_id] + str(hand_sign_id)
    cv.putText(image, info_text, (bounding_box[0] + 5, bounding_box[1] - 4), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)
    return image

# draw fps
def draw_fps(image, fps):
    cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv.LINE_AA)
    return image

if __name__ == "__main__":

    # Create two queues for inter-process communication
    queue = multiprocessing.Queue()

    # Create two processes for running the scripts
    print("Starting system.......")
    process1 = multiprocessing.Process(target=classifier_gesture, args=(queue,))
    print("Starting hand classifier.......")
    process2 = multiprocessing.Process(target=mainx, args=(queue,))
    print("Starting GUI system.......")
    # Start both processes
    process1.start()
    process2.start()
    #process2.start()

    # Wait for the GUI process to finish
    process1.join()
    process2.join()


    print("System closed")
