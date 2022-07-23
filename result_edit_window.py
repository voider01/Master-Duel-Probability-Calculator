import tkinter
import customtkinter as ctk
from utils import *

class result_edit_window(ctk.CTkToplevel):

    WIDTH = 600
    HEIGHT = 600

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Initiation/Result Edit")
        A = int(self.winfo_screenwidth()/2 - result_edit_window.WIDTH/2)
        B = int(self.winfo_screenheight()/2 - result_edit_window.HEIGHT/2)
        self.geometry(f"{result_edit_window.WIDTH}x{result_edit_window.HEIGHT}+{A}+{B}")
        self.iconbitmap("Galatea.ico")   # icon
        self.resizable(False, False)
        self.transient(parent)           # only use parent window

        self.inits=inits()

        # ============ create one frame ============        

        # configure grid layout (3x7)
        self.grid_rowconfigure(1, minsize=30)
        self.grid_rowconfigure((2, 3, 4, 5, 6), weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, minsize=20)

        self.notice_frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.notice_frame.grid(row=0, column=0, columnspan=3)

        self.notice = ctk.CTkLabel(master=self.notice_frame,
                                                   text="초동과 그 결과물을 입력할 수 있습니다.\n"
                                                   +"초동에 필요한 카드군과, 각 카드군에서 뽑아야 하는 카드 매수,\n"
                                                   +"한 카드군 내에서 카드를 뽑을 때 중복을 허용할지의 여부를 입력해주세요.\n\n"
                                                   +"예를 들어, 섀도르에는 '어둠 속성 섀도르 몬스터' 그룹에서 중복을 허용해 2장, \n"
                                                   +"'섀도르 퓨전/엘섀도르 퓨전' 그룹에서 1장을 뽑는 초동이 있습니다. (미도라시 엔드)\n\n"
                                                   +"단일 카드도 카드군처럼 사용할 수 있습니다.",
                                                   text_font=("맑은 고딕", 11),
                                                   width=result_edit_window.WIDTH,
                                                   height = 200,
                                                   anchor=tkinter.CENTER,
                                                   justify=tkinter.CENTER)
        self.notice.pack()

        self.res_frame = ctk.CTkFrame(master=self)
        self.res_frame.grid(row=2,column=0,rowspan=5,sticky='nswe', padx=20, pady=20)
        # configure grid layout (2x1)
        self.res_frame.grid_columnconfigure(0, weight=1)
        self.res_frame.grid_rowconfigure(0, weight=1)

        self.res_list_scrollbar = ctk.CTkScrollbar(master=self.res_frame)
        self.res_list = ctk.CTkTextbox(master=self.res_frame, text_font=("맑은 고딕", 12), yscrollcommand=self.res_list_scrollbar.set, state=tkinter.DISABLED)
        self.res_list.grid(row=0, column=0, sticky='nswe', padx=20, pady=20)
        
        self.res_list_scrollbar.grid(row=0, column=1, sticky='nswe', pady=20)
        self.res_list_scrollbar.configure(command=self.res_list.yview)

        self.load_res()
        self.refresh_inits()

        self.add_res_btn = ctk.CTkButton(master=self, text="초동 추가", text_font=("맑은 고딕", 11), height=40, fg_color='grey80', hover_color='grey50', command=self.add_res)
        self.add_res_btn.grid(row=2, column=1)

        self.edit_res_btn = ctk.CTkButton(master=self, text="초동 수정", text_font=("맑은 고딕", 11), height=40, fg_color='grey80', hover_color='grey50', command=self.edit_res)
        self.edit_res_btn.grid(row=3, column=1)

        self.delete_res_btn = ctk.CTkButton(master=self, text="초동 삭제", text_font=("맑은 고딕", 11), height=40, fg_color='grey80', hover_color='grey50', command=self.delete_res)
        self.delete_res_btn.grid(row=4, column=1)

        self.okay_btn = ctk.CTkButton(master=self, text="확인", text_font=("맑은 고딕", 11), height=40, command=self.save_res)
        self.okay_btn.grid(row=5, column=1)

        self.cancel_btn = ctk.CTkButton(master=self, text="취소", text_font=("맑은 고딕", 11), height=40, fg_color='grey80', hover_color='grey50', command=self.close_win)
        self.cancel_btn.grid(row=6, column=1)

    def add_res(self) :
        window = add_res(self)
        window.grab_set()
    
    def edit_res(self) :
        window = edit_res(self)
        window.grab_set()

    def delete_res(self) :
        window = delete_res(self)
        window.grab_set()

    def save_res(self) :
        self.parent.my_inits = self.inits
        self.parent.refresh_inits()
        self.destroy()
    
    def load_res(self):
        self.inits = self.parent.my_inits

    def refresh_inits(self):
        self.res_list.configure(state=tkinter.NORMAL)
        self.res_list.delete(0.0, "end")
        cnt=1
        for items in self.inits.init_list:
            self.res_list.insert("current", f"{cnt}. {items[1]}\n")
            cnt+=1
        self.res_list.delete("end-2c", "end")
        self.res_list.configure(state=tkinter.DISABLED)


    def close_win(self) : self.destroy()


class add_res(ctk.CTkToplevel):
    
    WIDTH = 500
    HEIGHT = 600

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Add Init/Res")
        A = int(self.winfo_screenwidth()/2 - add_res.WIDTH/2)
        B = int(self.winfo_screenheight()/2 - add_res.HEIGHT/2)
        self.geometry(f"{add_res.WIDTH}x{add_res.HEIGHT}+{A}+{B}")
        self.iconbitmap("Galatea.ico")   # icon
        self.resizable(False, False)
        self.transient(parent)

        # configure grid layout (7x8)
        self.grid_rowconfigure((1,3,5,7), minsize=20)
        self.grid_rowconfigure(9, minsize=15)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure((0,4), minsize=10)
        self.grid_columnconfigure(2, weight=1)

        self.notice_frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.notice_frame.grid(row=0, column=0, columnspan=5)

        self.notice = ctk.CTkLabel(master=self.notice_frame, text="총 필요 카드 매수가 6장 이하여야만 등록 가능합니다.", text_font=("맑은 고딕", 11), height=60, width=self.WIDTH)
        self.notice.grid(row=0, column=0, sticky='nswe')

        self.name_frame = ctk.CTkFrame(master=self)
        self.name_frame.grid(row=2, column=1, columnspan=4, sticky='nswe')

        self.name_frame.grid_columnconfigure(1, weight=1)
        self.name_frame.grid_columnconfigure(2, minsize=20)
        self.label_1 = ctk.CTkLabel(master=self.name_frame, text="이름", width=120, text_font=("맑은 고딕", 11, 'bold'))
        self.label_1.grid(row=0, column=0)

        self.init_name = ctk.CTkEntry(master=self.name_frame, text_font=("맑은 고딕", 11), placeholder_text="초동/결과 이름")
        self.init_name.grid(row=0, column=1, sticky='nswe', pady=5)


        self.checklist_frame = ctk.CTkFrame(master=self)
        self.checklist_frame.grid(row=4, column=1, columnspan=3, sticky='nswe')

        # ============== checklist_frame(6x10) (start) ==============
        self.checklist_frame.grid_rowconfigure((0,2,9),minsize=10)
        self.checklist_frame.grid_rowconfigure((3,4,5,6,7,8), weight=1)
        self.checklist_frame.grid_columnconfigure(2, weight=1)
        self.checklist_frame.grid_columnconfigure((0,5), minsize=10)

        ctk.CTkLabel(master=self.checklist_frame, text="번호", text_font=("맑은 고딕", 11, "bold"), width=50).grid(row=1, column=1, padx=10)
        ctk.CTkLabel(master=self.checklist_frame, text="카드/카드군", text_font=("맑은 고딕", 11, "bold")).grid(row=1, column=2)
        ctk.CTkLabel(master=self.checklist_frame, text="매수", text_font=("맑은 고딕", 11, "bold"), width=60).grid(row=1, column=3, padx=10)
        ctk.CTkLabel(master=self.checklist_frame, text="중복허용", text_font=("맑은 고딕", 11, "bold"), width=60).grid(row=1, column=4, padx=10)

        self.w_list=[]
        
        group_name = [a[0] for a in self.parent.parent.my_group] + ["단일 카드 선택"]

        for i in range(6):
            ctk.CTkLabel(master=self.checklist_frame,
                               text=f"{i+1}",
                               text_font=("맑은 고딕", 11),
                               width=50,
                               anchor='center').grid(row=3+i, column=1, padx=10, sticky='nswe')

            group_var = tkinter.StringVar()
            card_or_group_list = ctk.CTkOptionMenu(master=self.checklist_frame, values = group_name, text_font=("맑은 고딕", 10), dropdown_text_font=("맑은 고딕", 10), fg_color='white', button_color='grey60', variable=group_var, height=30, command=self.add_temp_group)
            card_or_group_list.grid(row=3+i, column=2, padx=10, sticky='we')

            nums_var=tkinter.StringVar(value="0")
            nums = ctk.CTkOptionMenu(master=self.checklist_frame, values = ['0','1','2','3','4','5','6'], text_font=("맑은 고딕", 10), dropdown_text_font=("맑은 고딕", 10), fg_color='white', variable=nums_var, width=60, button_color='grey60', height=30)
            nums.grid(row=3+i, column=3, padx=10, sticky='we')

            cb_var = tkinter.IntVar()
            cb = ctk.CTkCheckBox(master=self.checklist_frame, onvalue=1, offvalue=0, variable=cb_var, text="")
            cb.grid(row=3+i, column=4)   

            self.w_list.append((group_var, nums_var, cb_var))

        self.selected_row = -1
        # ============== checklist_frame(end) ==============
        
        self.res_frame = ctk.CTkFrame(master=self)
        self.res_frame.grid(row=6, column=1, columnspan=3, sticky='nswe')

        self.res_frame.grid_columnconfigure(1, weight=1)
        self.res_frame.grid_columnconfigure(2, minsize=20)
        self.label_1 = ctk.CTkLabel(master=self.res_frame, text="결과물", width=120, text_font=("맑은 고딕", 11, 'bold'))
        self.label_1.grid(row=0, column=0)

        self.res = ctk.CTkEntry(master=self.res_frame, text_font=("맑은 고딕", 11), placeholder_text="간단히 최종 필드/자원 등을 기재")
        self.res.grid(row=0, column=1, sticky='nswe', pady=5)

        self.okay_btn = ctk.CTkButton(master=self, text="확인", text_font=("맑은 고딕", 11), width=130, command=self.add_init)
        self.okay_btn.grid(row=8, column=1, sticky='nsw')

        self.cancel_btn = ctk.CTkButton(master=self, text="취소", text_font=("맑은 고딕", 11), fg_color='grey80', hover_color='grey50', width=130, command=self.close_win)
        self.cancel_btn.grid(row=8, column=3, sticky='nse')

    def add_init(self):
        d1 = self.parent.parent.my_deck.get_name_to_idx_dict()
        d2 = self.parent.parent.my_group.get_name_to_idx_dict()
        total_card_num = 0
        temp = []
        temp_string = []
        for w in self.w_list:       # w.list : list of (group_or_card_name StringVar, # of cards StringVar, checkbox IntVar)
            nums = int(w[1].get())
            if nums != 0: 
                name = w[0].get()
                if nums==1: permission = 0
                else: permission = w[2].get()
                if name in d1.keys():
                    temp.append([[d1[w[0].get()]], nums, permission])
                else:
                    temp.append([d2[w[0].get()], nums, permission])
                temp_string.append([name, nums, permission])
            total_card_num+=nums

        if total_card_num<=0 or total_card_num>6: pass
        else:
            self.parent.inits.add(temp, temp_string, self.init_name.get(), self.res.get(), total_card_num)    
            """
            inits : list of [init, name, res, tot]
                name : name of init/res pair
                init : list of [idx_list, num, per]
                    idx_list : list of card_idx
                    num : # of requiring cards
                    per : permission, if 1, duplication allowed / if 0, disallowed.
                res : result String
                tot : total card_num
            """
            self.parent.refresh_inits()
            self.destroy()

    def add_temp_group(self, group_name):
        if group_name != "단일 카드 선택": pass
        else:
            for i in range(6):
                if self.w_list[i][0].get() == "단일 카드 선택": self.selected_row = i
            window = add_temp_group(self)
            window.grab_set()

    def close_win(self): self.destroy()



class add_temp_group(ctk.CTkToplevel):
    
    WIDTH = 450
    HEIGHT = 300

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Pick 1 card")
        A = int(self.winfo_screenwidth()/2 - add_temp_group.WIDTH/2)
        B = int(self.winfo_screenheight()/2 - add_temp_group.HEIGHT/2)
        self.geometry(f"{add_temp_group.WIDTH}x{add_temp_group.HEIGHT}+{A}+{B}")
        self.iconbitmap("Galatea.ico")   # icon
        self.resizable(False, False)
        self.transient(parent)           # only use parent window

        # configure grid layout (5x6)        
        self.grid_rowconfigure((1,3), minsize=20)
        self.grid_rowconfigure(6, minsize=10)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure((0,5), minsize=20)
        self.grid_columnconfigure(2, weight=1)

        self.notice_frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.notice_frame.grid(row=0, column=0, columnspan=6)

        self.notice = ctk.CTkLabel(master=self.notice_frame, text="원하는 카드를 골라주세요.", text_font=("맑은 고딕", 11), height=60, width=self.WIDTH)
        self.notice.grid(row=0, column=0, columnspan=3, sticky='nswe')

        card_dict={}
        for card in self.parent.parent.parent.my_deck:
            for i in range(len(self.parent.parent.parent.my_deck.cards)):
                card_dict[card[0]] = i
        card_list=list(card_dict.keys())

        self.card_var = tkinter.StringVar()
        self.single_card = ctk.CTkOptionMenu(master=self, values = card_list, text_font=("맑은 고딕", 11), dropdown_text_font=("맑은 고딕", 11), fg_color='white', variable=self.card_var, width=300, button_color='grey60', height=40, dynamic_resizing=False)
        self.single_card.grid(row=2, column=1, columnspan=3)

        self.okay_btn = ctk.CTkButton(master=self, text="확인", text_font=("맑은 고딕", 11), width=130, height=35, command=self.select_single_card)
        self.okay_btn.grid(row=4, column=1, sticky='nsw')

        self.cancel_btn = ctk.CTkButton(master=self, text="취소", text_font=("맑은 고딕", 11), height=35, fg_color='grey80', hover_color='grey50', width=130, command=self.close_win)
        self.cancel_btn.grid(row=4, column=3, sticky='nse')


    def select_single_card(self):
        self.parent.w_list[self.parent.selected_row][0].set(self.card_var.get())
        self.parent.w_list[self.parent.selected_row][2].set(1)
        self.parent.selected_row=-1
        self.destroy()

    def close_win(self):
        self.parent.selected_row=-1
        self.destroy()

class edit_res(ctk.CTkToplevel):
    
    WIDTH = 500
    HEIGHT = 600

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Edit Init/Res")
        A = int(self.winfo_screenwidth()/2 - edit_res.WIDTH/2)
        B = int(self.winfo_screenheight()/2 - edit_res.HEIGHT/2)
        self.geometry(f"{edit_res.WIDTH}x{edit_res.HEIGHT}+{A}+{B}")
        self.iconbitmap("Galatea.ico")   # icon
        self.resizable(False, False)
        self.transient(parent)

        # configure grid layout (7x8)
        self.grid_rowconfigure((1,3,5,7), minsize=20)
        self.grid_rowconfigure(9, minsize=15)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure((0,4), minsize=10)
        self.grid_columnconfigure(2, weight=1)

        self.notice_frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.notice_frame.grid(row=0, column=0, columnspan=5)

        self.notice = ctk.CTkLabel(master=self.notice_frame, text="수정할 초동을 선택하고, 수정 후 확인 버튼을 눌러주세요.", text_font=("맑은 고딕", 11), height=60, width=self.WIDTH)
        self.notice.grid(row=0, column=0, sticky='nswe')

        self.name_frame = ctk.CTkFrame(master=self)
        self.name_frame.grid(row=2, column=1, columnspan=4, sticky='nswe')

        self.name_frame.grid_columnconfigure(1, weight=1)
        self.name_frame.grid_columnconfigure(2, minsize=20)
        self.label_1 = ctk.CTkLabel(master=self.name_frame, text="초동", width=120, text_font=("맑은 고딕", 11, 'bold'))
        self.label_1.grid(row=0, column=0)

        init_names = [a[1] for a in self.parent.inits.init_list]

        self.var = tkinter.StringVar(value="초동 선택")
        self.init_name = ctk.CTkOptionMenu(master=self.name_frame, values = init_names, variable=self.var, text_font=("맑은 고딕", 10), dropdown_text_font=("맑은 고딕", 10), fg_color='white', button_color='grey60', command=self.load_init)
        self.init_name.grid(row=0, column=1, sticky='nswe', pady=5)

        self.checklist_frame = ctk.CTkFrame(master=self)
        self.checklist_frame.grid(row=4, column=1, columnspan=3, sticky='nswe')

        # ============== checklist_frame(6x10) (start) ==============
        self.checklist_frame.grid_rowconfigure((0,2,9),minsize=10)
        self.checklist_frame.grid_rowconfigure((3,4,5,6,7,8), weight=1)
        self.checklist_frame.grid_columnconfigure(2, weight=1)
        self.checklist_frame.grid_columnconfigure((0,5), minsize=10)

        ctk.CTkLabel(master=self.checklist_frame, text="번호", text_font=("맑은 고딕", 11, "bold"), width=50).grid(row=1, column=1, padx=10)
        ctk.CTkLabel(master=self.checklist_frame, text="카드/카드군", text_font=("맑은 고딕", 11, "bold")).grid(row=1, column=2)
        ctk.CTkLabel(master=self.checklist_frame, text="매수", text_font=("맑은 고딕", 11, "bold"), width=60).grid(row=1, column=3, padx=10)
        ctk.CTkLabel(master=self.checklist_frame, text="중복허용", text_font=("맑은 고딕", 11, "bold"), width=60).grid(row=1, column=4, padx=10)

        self.w_list=[]
        
        init_name = [a[0] for a in self.parent.parent.my_group] + ["단일 카드 선택"]

        for i in range(6):
            ctk.CTkLabel(master=self.checklist_frame,
                               text=f"{i+1}",
                               text_font=("맑은 고딕", 11),
                               width=50,
                               anchor='center').grid(row=3+i, column=1, padx=10, sticky='nswe')

            group_var = tkinter.StringVar()
            card_or_group_list = ctk.CTkOptionMenu(master=self.checklist_frame, values = init_name, text_font=("맑은 고딕", 10), dropdown_text_font=("맑은 고딕", 10), fg_color='white', button_color='grey60', variable=group_var, height=30, command=self.add_temp_group)
            card_or_group_list.grid(row=3+i, column=2, padx=10, sticky='we')

            nums_var=tkinter.StringVar(value="0")
            nums = ctk.CTkOptionMenu(master=self.checklist_frame, values = ['0','1','2','3','4','5','6'], text_font=("맑은 고딕", 10), dropdown_text_font=("맑은 고딕", 10), fg_color='white', variable=nums_var, width=60, button_color='grey60', height=30)
            nums.grid(row=3+i, column=3, padx=10, sticky='we')

            cb_var = tkinter.IntVar()
            cb = ctk.CTkCheckBox(master=self.checklist_frame, onvalue=1, offvalue=0, variable=cb_var, text="")
            cb.grid(row=3+i, column=4)   

            self.w_list.append((group_var, nums_var, cb_var))

        self.selected_row = -1
        # ============== res_frame(end) ==============
        
        self.res_frame = ctk.CTkFrame(master=self)
        self.res_frame.grid(row=6, column=1, columnspan=3, sticky='nswe')

        self.res_frame.grid_columnconfigure(1, weight=1)
        self.res_frame.grid_columnconfigure(2, minsize=20)
        self.label_1 = ctk.CTkLabel(master=self.res_frame, text="결과물", width=120, text_font=("맑은 고딕", 11, 'bold'))
        self.label_1.grid(row=0, column=0)

        self.res = ctk.CTkEntry(master=self.res_frame, text_font=("맑은 고딕", 11), placeholder_text="간단히 최종 필드/자원 등을 기재")
        self.res.grid(row=0, column=1, sticky='nswe', pady=5)

        self.okay_btn = ctk.CTkButton(master=self, text="확인", text_font=("맑은 고딕", 11), width=130, command=self.edit_init)
        self.okay_btn.grid(row=8, column=1, sticky='nsw')

        self.cancel_btn = ctk.CTkButton(master=self, text="취소", text_font=("맑은 고딕", 11), fg_color='grey80', hover_color='grey50', width=130, command=self.close_win)
        self.cancel_btn.grid(row=8, column=3, sticky='nse')

    def load_init(self, name):
        d = self.parent.inits.get_name_to_string_list_dict()
        dd = d[name][0]
        for i in range(len(dd)):
            self.w_list[i][0].set(dd[i][0])
            self.w_list[i][1].set(str(dd[i][1]))
            self.w_list[i][2].set(dd[i][2])
        for i in range(len(dd), 6):
            self.w_list[i][0].set('')
            self.w_list[i][1].set('0')
            self.w_list[i][2].set(0)
        self.res.delete(0, "end")
        self.res.insert(0, d[name][2])       

    def edit_init(self):
        if self.var.get()=='초동 선택':pass
        d = self.parent.parent.my_inits.get_name_to_idx_dict()
        d1 = self.parent.parent.my_deck.get_name_to_idx_dict()
        d2 = self.parent.parent.my_group.get_name_to_idx_dict()
        total_card_num = 0
        temp = []
        temp_string = []
        for w in self.w_list:       # w.list : list of (group_or_card_name StringVar, # of cards StringVar, checkbox IntVar)
            nums = int(w[1].get())
            if nums != 0: 
                name = w[0].get()
                if nums==1: permission = 0
                else: permission = w[2].get()
                if name in d1.keys():
                    temp.append([[d1[w[0].get()]], nums, permission])
                else:
                    temp.append([d2[w[0].get()], nums, permission])
                temp_string.append([name, nums, permission])
            total_card_num+=nums

        if total_card_num<=0 or total_card_num>6: pass
        else:
            self.parent.inits.edit(d[self.var.get()], temp, temp_string, self.init_name.get(), self.res.get(), total_card_num)    
            """
            inits : list of [init, name, res, tot]
                name : name of init/res pair
                init : list of [idx_list, num, per]
                    idx_list : list of card_idx
                    num : # of requiring cards
                    per : permission, if 1, duplication allowed / if 0, disallowed.
                res : result String
                tot : total card_num
            """
            self.parent.refresh_inits()
            self.destroy()
 
    def add_temp_group(self, group_name):
        if group_name != "단일 카드 선택": pass
        else:
            for i in range(6):
                if self.w_list[i][0].get() == "단일 카드 선택": self.selected_row = i
            window = add_temp_group(self)
            window.grab_set()

    def close_win(self): self.destroy()


class delete_res(ctk.CTkToplevel):
        
    WIDTH = 450
    HEIGHT = 400

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Delete Init/Res pair")
        A = int(self.winfo_screenwidth()/2 - delete_res.WIDTH/2)
        B = int(self.winfo_screenheight()/2 - delete_res.HEIGHT/2)
        self.geometry(f"{delete_res.WIDTH}x{delete_res.HEIGHT}+{A}+{B}")
        self.iconbitmap("Galatea.ico")   # icon
        self.resizable(False, False)
        self.transient(parent)
      
        # configure grid layout (6x6)        
        self.grid_rowconfigure(1, minsize=20)
        self.grid_rowconfigure((3,5), minsize=10)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure((0,5), minsize=20)
        self.grid_columnconfigure(2, weight=1)

        self.notice_frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.notice_frame.grid(row=0, column=0, columnspan=6)

        self.notice = ctk.CTkLabel(master=self.notice_frame, text="삭제할 초동을 선택하고 삭제 버튼을 눌러주세요.", text_font=("맑은 고딕", 11), height=60, width=self.WIDTH)
        self.notice.grid(row=0, column=0, columnspan=3, sticky='nswe')

        self.checklist_canvas = ctk.CTkCanvas(master=self, background='white', height=200, bg='#DEDEDE')
        self.checklist_canvas.grid(row=2, column=1, columnspan=3, sticky='nswe')

        self.canvas_scrollbar = ctk.CTkScrollbar(master=self, orientation='vertical', command=self.checklist_canvas.yview)
        self.canvas_scrollbar.grid(row=2, column=4, sticky='nse')

        self.checklist_canvas.bind('<Configure>', lambda e: self.checklist_canvas.configure(scrollregion = self.checklist_canvas.bbox('all')))

        self.canvasframe = ctk.CTkFrame(master=self.checklist_canvas, corner_radius=0)
        self.canvasframe.grid_columnconfigure(0, weight=1)

        self.checklist_canvas.configure(yscrollcommand=self.canvas_scrollbar.set)
        self.checklist_canvas.create_window((0,0), window=self.canvasframe, width=380, anchor='nw')

        self.checklist_canvas.pack_propagate(0)

        self.init_list=[]
        for data in self.parent.inits.init_string_list:
            self.init_list.append(data[1])

        self.boxes = ChecklistBox(self.canvasframe, self.init_list)

        self.okay_btn = ctk.CTkButton(master=self, text="삭제", text_font=("맑은 고딕", 11), width=130, height=40, command=self.delete_init)
        self.okay_btn.grid(row=4, column=1, sticky='nsw')

        self.cancel_btn = ctk.CTkButton(master=self, text="취소", text_font=("맑은 고딕", 11), fg_color='grey80', hover_color='grey50', width=130, height=40, command=self.close_win)
        self.cancel_btn.grid(row=4, column=3, sticky='nse', columnspan=2)

    def delete_init(self):
        indices = [i for i in range(len(self.init_list)) if not i in self.boxes.getCheckedIdx()]
        new_inits1 = []
        new_inits2 = []
        for idx in indices:
            new_inits1.append(self.parent.inits.init_list[idx])
            new_inits2.append(self.parent.inits.init_string_list[idx])
        self.parent.inits.init_list = new_inits1
        self.parent.inits.init_string_list = new_inits2

        self.parent.refresh_inits()
        self.destroy()

    def close_win(self): self.destroy()