import tkinter
import customtkinter as ctk
from utils import *

class deck_edit_window(ctk.CTkToplevel):
    
    WIDTH = 600
    HEIGHT = 600

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Deck Edit")
        A = int(self.winfo_screenwidth()/2 - deck_edit_window.WIDTH/2)
        B = int(self.winfo_screenheight()/2 - deck_edit_window.HEIGHT/2)
        self.geometry(f"{deck_edit_window.WIDTH}x{deck_edit_window.HEIGHT}+{A}+{B}")
        self.iconbitmap("Galatea.ico")   # icon
        self.resizable(False, False)
        self.transient(parent)           # only use parent window

        # ============ create one frame ============        

        # configure grid layout (4x3)

        self.grid_rowconfigure((1, 2), weight=1)

        self.notice_frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.notice_frame.grid(row=0, column=0, columnspan=4)

        self.decklist_frame = ctk.CTkFrame(master=self)
        self.decklist_frame.grid(row=1, column=0, sticky="nswe", pady=20, columnspan=4)
        self.decklist_frame.grid_columnconfigure(1, weight=1)

        self.notice = ctk.CTkLabel(master=self.notice_frame,
                                                   text="표에 카드명과 카드 매수를 입력한 뒤\n"
                                                   +"확인 버튼을 누르면 덱 리스트가 수정됩니다.\n"+
                                                   "칸이 모자랄 경우 '다음' 버튼을 눌러주세요.",
                                                   text_font=("맑은 고딕", 11),
                                                   width=deck_edit_window.WIDTH,
                                                   height = 100,
                                                   anchor=tkinter.CENTER,
                                                   justify=tkinter.CENTER)
        self.notice.pack()

        ctk.CTkLabel(master=self.decklist_frame, text="번호", text_font=("맑은 고딕", 11, "bold"), width=80).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(master=self.decklist_frame, text="카드명", text_font=("맑은 고딕", 11, "bold")).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkLabel(master=self.decklist_frame, text="매수", text_font=("맑은 고딕", 11, "bold"), width=80).grid(row=0, column=2, padx=10, pady=5)

        self.cur_page_num = 1
        self.card_data_dict=dict()
        self.make_entrys_init()
        self.load_my_deck()
        self.load_temp()

        self.prev_button = ctk.CTkButton(master = self,
                                         text="이전",
                                         height=35,
                                         text_font=("맑은 고딕", 11),
                                         fg_color='grey80',
                                         hover_color='grey50',
                                         command=self.prev_list)
        self.prev_button.grid(row=2, column=0, pady=15)

        self.ok_button = ctk.CTkButton(master = self,
                                       text="확인",
                                       height=35,
                                       text_font=("맑은 고딕", 11),
                                       command = self.save_deck_list)
        self.ok_button.grid(row=2, column=1, pady=15)

        self.cancel_button = ctk.CTkButton(master = self,
                                           text="취소",
                                           height=35,
                                           text_font=("맑은 고딕", 11),
                                           fg_color='grey80',
                                           hover_color='grey50',
                                           command = self.close_win)
        self.cancel_button.grid(row=2, column=2, pady=15) 

        self.next_button = ctk.CTkButton(master = self,
                                         text="다음",
                                         height=35,
                                         text_font=("맑은 고딕", 11),
                                         fg_color='grey80',
                                         hover_color='grey50',
                                         command=self.next_list)
        self.next_button.grid(row=2, column=3, pady=15)

        # Disable prev if page 1
        self.button_active()



    def prev_or_next(self, num):
        self.save_temp()
        self.cur_page_num+=num
        self.load_temp()
        self.refresh_idx()
        self.button_active()
        self.w_list[0][1].focus_set()

    def prev_list(self): self.prev_or_next(-1)
    def next_list(self): self.prev_or_next(1)

    def button_active(self):
        if self.cur_page_num == 1 : self.prev_button.configure(state = tkinter.DISABLED)
        elif self.cur_page_num == 6 : self.next_button.configure(state = tkinter.DISABLED)
        else :
            self.prev_button.configure(state = tkinter.NORMAL)
            self.next_button.configure(state = tkinter.NORMAL)
    
    def make_entrys_init(self):
        self.w_list=[]
        for i in range(1, 11):
            idx = ctk.CTkLabel(master=self.decklist_frame,
                        text=f"{10*(self.cur_page_num-1)+i}",
                        text_font=("맑은 고딕", 11),
                        width=80,
                        anchor=tkinter.CENTER)
            idx.grid(row=i, column=0)
            card_name = ctk.CTkEntry(master=self.decklist_frame, text_font=("맑은 고딕", 10))
            card_name.grid(row=i, column=1, sticky="nswe", pady=3, padx=10)
            card_num = ctk.CTkComboBox(master=self.decklist_frame,
                                       text_font=("맑은 고딕", 10),
                                       values=["0", "1", "2", "3"],
                                       width=80,
                                       state="readonly",
                                       takefocus=-1)
            card_num.set("0")
            card_num.grid(row=i, column=2)
            self.w_list.append((idx, card_name, card_num))
            for w in self.w_list:
                w[1].lift()
       

    def refresh_idx(self):
        for i in range(1, 11):
            self.w_list[i-1][0].configure(text=f"{10*(self.cur_page_num-1)+i}")
        
    
    def save_temp(self):
        for i in range(1, 11):
            self.card_data_dict[10*(self.cur_page_num-1)+i] = \
                (self.w_list[i-1][1].get(), int(self.w_list[i-1][2].get()))

    def load_temp(self):
        for i in range(10):
            nums = 10*(self.cur_page_num-1) + i+1
            if nums in self.card_data_dict:
                self.w_list[i][1].delete(0, tkinter.END)
                self.w_list[i][1].insert(0, self.card_data_dict[nums][0])
                self.w_list[i][2].set(str(self.card_data_dict[nums][1]))
            else:
                self.w_list[i][1].delete(0, tkinter.END)
                self.w_list[i][2].set("0")

    def close_win(self): self.destroy()

    def save_deck_list(self):
        self.save_temp()
        self.parent.my_deck.clear()
        for pair in self.card_data_dict.values():
            if pair[1]>0: self.parent.my_deck.add_card(pair[0], pair[1])
        self.parent.my_deck.valid()
        self.parent.refresh_decklist()        
        self.destroy()

    def load_my_deck(self):
        cnt=1
        for data in self.parent.my_deck:        # data : (card name, #s)
            self.card_data_dict[cnt] = (data[0], data[1])
            cnt+=1