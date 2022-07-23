import ctypes
import pickle
import tkinter
import tkinter.filedialog
import customtkinter as ctk

from utils import *
from deck_edit_window import *
from group_edit_window import *
from result_edit_window import *
from calc_prob_window import *


myappid = 'arbitrary string' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    
    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.title("Master Duel Probability Calculator")
        A = int(self.winfo_screenwidth()/2 - App.WIDTH/2)
        B = int(self.winfo_screenheight()/2 - App.HEIGHT/2)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}+{A}+{B}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        self.iconbitmap("Galatea.ico")   # icon
        self.resizable(False, False)

        self.my_deck = deck()
        self.my_group = groups()
        self.my_inits = inits()

        # ============ create two frames ============

        # configure grid layout (2x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.frame_left = ctk.CTkFrame(master=self, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe", rowspan=2)

        self.frame_right_1 = ctk.CTkFrame(master=self)
        self.frame_right_1.grid(row=0, column=1, sticky="nswe", padx=20, pady=10)
        self.frame_right_2 = ctk.CTkFrame(master=self)
        self.frame_right_2.grid(row=1, column=1, sticky="nswe", padx=20, pady=10)

        # ============ frame_left ============

        # configure grid layout (1x8)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(6, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(9, minsize=20)  # empty row with minsize as spacing

        self.label_1 = ctk.CTkLabel(master=self.frame_left,
                                            text="메뉴",
                                            text_font=("맑은 고딕", 20, 'bold'))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = ctk.CTkButton(master=self.frame_left,
                                            text="덱 리스트 수정",
                                            height=40,
                                            text_font=("맑은 고딕", 11),
                                            command=self.open_deck_edit)
        self.button_1.grid(row=2, column=0, pady=15, padx=20)

        self.button_2 = ctk.CTkButton(master=self.frame_left,
                                            text="카드군 수정",
                                            height=40,
                                            text_font=("맑은 고딕", 11),
                                            command=self.open_group_edit)
        self.button_2.grid(row=3, column=0, pady=15, padx=20)

        self.button_3 = ctk.CTkButton(master=self.frame_left,
                                            text="초동/결과물 수정",
                                            height=40,
                                            text_font=("맑은 고딕", 11),
                                            command=self.open_result_edit)
        self.button_3.grid(row=4, column=0, pady=15, padx=20)

        self.button_4 = ctk.CTkButton(master=self.frame_left,
                                            text="초동률 계산",
                                            height=40,
                                            text_font=("맑은 고딕", 11),
                                            command=self.open_calc_prob)
        self.button_4.grid(row=5, column=0, pady=15, padx=20)

        self.button_5 = ctk.CTkButton(master=self.frame_left,
                                            text="불러오기",
                                            height=40,
                                            text_font=("맑은 고딕", 11),
                                            command=self.load_data)
        self.button_5.grid(row=7, column=0, pady=15, padx=20)

        self.button_6 = ctk.CTkButton(master=self.frame_left,
                                            text="저장하기",
                                            height=40,
                                            text_font=("맑은 고딕", 11),
                                            command=self.save_data)
        self.button_6.grid(row=8, column=0, pady=15, padx=20)

        # ============ frame_right_1 ============

        # configure grid layout (1x1)
        self.frame_right_1.grid_columnconfigure(0, weight=1)
        self.frame_right_1.grid_rowconfigure(1, weight=1)
        self.frame_right_1.grid_rowconfigure(2, minsize=20)

        self.notice_1 = ctk.CTkLabel(master=self.frame_right_1,
                                   text_font=("맑은 고딕", 18, 'bold'),
                                   text="덱 리스트")
        
        self.notice_1.grid(row=0, column=0, pady=10, sticky='nswe')

        self.addi_frame_1 = ctk.CTkFrame(master=self.frame_right_1)
        self.addi_frame_1.grid(row=1, column=0, sticky='nswe', padx=20)

        self.addi_frame_1.grid_rowconfigure(0, weight=1)
        self.addi_frame_1.grid_columnconfigure(0, weight=1)
        self.deck_list = ctk.CTkTextbox(master=self.addi_frame_1,
                                        text_font=("맑은 고딕", 11),
                                        height=8,
                                        state=tkinter.DISABLED)
        self.deck_list.grid(row=0, column=0, sticky='nswe', padx=20, pady=20)

        

        # ============ frame_right_2 ============
        self.frame_right_2.grid_columnconfigure(0, weight=1)
        self.frame_right_2.grid_rowconfigure(1, weight=1)
        self.frame_right_2.grid_rowconfigure(2, minsize=20)

        self.notice_2 = ctk.CTkLabel(master=self.frame_right_2,
                                   text_font=("맑은 고딕", 18, 'bold'),
                                   text="초동/결과물 리스트")
        
        self.notice_2.grid(row=0, column=0, pady=10, sticky='nswe')

        self.addi_frame_2 = ctk.CTkFrame(master=self.frame_right_2)
        self.addi_frame_2.grid(row=1, column=0, sticky='nswe', padx=20)

        self.addi_frame_2.grid_rowconfigure(0, weight=1)
        self.addi_frame_2.grid_columnconfigure(0, weight=1)
        self.result_list = ctk.CTkTextbox(master=self.addi_frame_2,
                                        text_font=("맑은 고딕", 11),
                                        height=8,
                                        state=tkinter.DISABLED)
        self.result_list.grid(row=0, column=0, sticky='nswe', padx=20, pady=20)


    def open_deck_edit(self):
        window = deck_edit_window(self)
        window.grab_set()           # only manipulate topmost window

    def open_group_edit(self):
        window = group_edit_window(self)
        window.grab_set()        

    def open_result_edit(self):
        window = result_edit_window(self)
        window.grab_set()

    def open_calc_prob(self):
        window = calc_prob_window(self)
        window.grab_set()

    def load_data(self):
        filename = tkinter.filedialog.askopenfilename(initialdir="", title="Save deck list",
                                          filetypes=(("pickle", "*.pkl"), 
                                          ("all files", "*.*")))
        if filename !="":        
            with open(filename,"rb") as fr:
                data = pickle.load(fr)
            self.my_deck = data[0]
            self.my_group = data[1]
            self.my_inits = data[2]
            self.refresh_decklist()
            self.refresh_inits()

    def save_data(self):
        filename = tkinter.filedialog.asksaveasfilename(initialdir="", title="Save deck list",
                                          filetypes=(("pickle", "*.pkl"), 
                                          ("all files", "*.*")))

        if filename[-4:]==".pkl" : filename=filename[:len(filename)-4]

        if filename != "":
            with open(filename+".pkl","wb") as fw:
                pickle.dump([self.my_deck, self.my_group, self.my_inits], fw)

    def on_closing(self, event=0):
        self.destroy()

    def refresh_decklist(self):
        self.deck_list.configure(state=tkinter.NORMAL)
        self.deck_list.delete(0.0, "end")
        for data in self.my_deck:
            self.deck_list.insert("current", " "+data[0]+" × "+str(data[1])+"\n")
        self.deck_list.delete("end-2c", "end")
        self.deck_list.configure(state=tkinter.DISABLED)

    def refresh_inits(self):
        self.result_list.configure(state=tkinter.NORMAL)
        self.result_list.delete(0.0, "end")
        cnt=1
        for data in self.my_inits.init_string_list:     # data : [inits_string, name, result, tot]
            self.result_list.insert("current", f"{cnt}. "+data[1]+f": {data[3]}핸드  ==>  "+data[2]+"\n   (")
            for data_m in data[0]:                                        # inits_string: [name, nums, permission]
                if data_m[1]<=1: self.result_list.insert("current", f"{data_m[0]} {data_m[1]}장, ")
                elif data_m[2]==1 : self.result_list.insert("current", f"{data_m[0]} {data_m[1]}장(중복 가능), ")
                else: self.result_list.insert("current", f"{data_m[0]} {data_m[1]}장(중복 불가), ")
            self.result_list.delete("end-3c", "end")
            self.result_list.insert("current", ")\n\n")
            cnt+=1
        self.result_list.delete("end-3c", "end")
        self.result_list.configure(state=tkinter.DISABLED)

if __name__ == "__main__":
    app = App()
    app.mainloop()

