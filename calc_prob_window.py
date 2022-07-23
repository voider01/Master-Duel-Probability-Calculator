from itertools import combinations, product, combinations_with_replacement
import tkinter
import customtkinter as ctk
from utils import *

class calc_prob_window(ctk.CTkToplevel):
    
    WIDTH = 600
    HEIGHT = 600

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Calculate!!")
        A = int(self.winfo_screenwidth()/2 - calc_prob_window.WIDTH/2)
        B = int(self.winfo_screenheight()/2 - calc_prob_window.HEIGHT/2)
        self.geometry(f"{calc_prob_window.WIDTH}x{calc_prob_window.HEIGHT}+{A}+{B}")
        self.iconbitmap("Galatea.ico")   # icon
        self.resizable(False, False)
        self.transient(parent)

        self.customs=[]

        # configure grid layout (5x4)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=10)
        self.grid_columnconfigure((0,4), minsize=20)
        self.grid_columnconfigure((1,3), weight=1)

        self.notice_frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.notice_frame.grid(row=0, column=0, columnspan=5)

        self.notice = ctk.CTkLabel(master=self.notice_frame,
                                                   text="옵션 선택 후 계산 버튼을 누르면 해당 초동을 잡을 확률을 계산합니다.\n"
                                                   +"추가 계산 항목 버튼을 이용해 여러 초동 중 \n"
                                                   +"하나라도 잡을 확률을 구할 수도 있습니다.",
                                                   text_font=("맑은 고딕", 11),
                                                   width=calc_prob_window.WIDTH,
                                                   height = 100,
                                                   anchor=tkinter.CENTER,
                                                   justify=tkinter.CENTER)
        self.notice.pack()

        self.res_frame = ctk.CTkFrame(master=self)
        self.res_frame.grid(row=1,column=1, columnspan=3, sticky='nswe', padx=20, pady=20)
        #==========configure grid layout (2x1)==============
        self.res_frame.grid_columnconfigure(0, weight=1)
        self.res_frame.grid_rowconfigure(0, weight=1)
        
        self.checklist_canvas = ctk.CTkCanvas(master=self.res_frame, background='white', height=150, bg='#DEDEDE')
        self.checklist_canvas.grid(row=0, column=0, sticky='nswe')

        self.canvas_scrollbar = ctk.CTkScrollbar(master=self.res_frame, orientation='vertical', height=150, command=self.checklist_canvas.yview)
        self.canvas_scrollbar.grid(row=0, column=1, sticky='nse')

        self.checklist_canvas.bind('<Configure>', lambda e: self.checklist_canvas.configure(scrollregion = self.checklist_canvas.bbox('all')))

        self.canvasframe = ctk.CTkFrame(master=self.checklist_canvas, corner_radius=0)
        self.canvasframe.grid_columnconfigure(0, weight=1)

        self.checklist_canvas.configure(yscrollcommand=self.canvas_scrollbar.set)
        self.checklist_canvas.create_window((0,0), window=self.canvasframe, width=500, anchor='nw')

        self.names_list=[]
        for items in self.parent.my_inits.init_list:
            self.names_list.append(items[1])
        if len(self.names_list) >=2 : self.names_list.append("전체 확률")
        self.boxes = ChecklistBox(self.canvasframe, self.names_list, select=1)

        #=============================================

        # Option_frame (7x7)        
        self.option_frame = ctk.CTkFrame(master=self)
        self.option_frame.grid(row=2, column=1, columnspan=3, padx=20, pady=10, sticky='nswe')
        self.option_frame.grid_rowconfigure((3,5), weight=1)
        self.option_frame.grid_rowconfigure((0,2,4,6), minsize=20)
        self.option_frame.grid_columnconfigure((1,3,5), weight=1)
        self.option_frame.grid_columnconfigure((0,2,4,6), minsize=25)

        self.first_second_frame = ctk.CTkFrame(master=self.option_frame)
        self.first_second_frame.grid(row=1, column=1, columnspan=3, sticky='nswe')
        self.first_second_frame.grid_rowconfigure(0, weight=1)
        self.first_second_frame.grid_columnconfigure(1, weight=1)

        self.first_second_label = ctk.CTkLabel(master=self.first_second_frame, text="선후공", text_font=("맑은 고딕", 11, 'bold'), width=100, height=25)
        self.first_second_label.grid(row=0, column=0, padx=10, pady=10, sticky='nswe')

        self.first_second_var = tkinter.StringVar(value = "선공 (5장)")
        self.first_second = ctk.CTkOptionMenu(master=self.first_second_frame, values = ["선공 (5장)", "후공 (6장)"], text_font=("맑은 고딕", 10), dropdown_text_font=("맑은 고딕", 10), fg_color='white', button_color='grey60', variable=self.first_second_var, height=28, dynamic_resizing=False)
        self.first_second.grid(row=0, column=1, padx=10, pady=7, sticky='nswe')

        self.add_btn = ctk.CTkButton(master=self.option_frame, text="계산 추가", text_font=("맑은 고딕", 11), fg_color='grey80', hover_color='grey50', width=140, height=35, command=self.add_custom)
        self.add_btn.grid(row=3, column=1)

        self.delete_btn = ctk.CTkButton(master=self.option_frame, text="계산 삭제", text_font=("맑은 고딕", 11), fg_color='grey80', hover_color='grey50', width=140, height=35, command=self.delete_custom)
        self.delete_btn.grid(row=3, column=3)

        self.handtrap = ctk.CTkButton(master=self.option_frame, text="상대 패트랩 옵션", text_font=("맑은 고딕", 11), fg_color='grey80', hover_color='grey50', width=140, height=35, state=tkinter.DISABLED)
        self.handtrap.grid(row=3, column=5)

        self.pot = ctk.CTkButton(master=self.option_frame, text="항아리 사용 규칙", text_font=("맑은 고딕", 11), fg_color='grey80', hover_color='grey50', width=140, height=35, state=tkinter.DISABLED)
        self.pot.grid(row=5, column=1)

        self.random_init = ctk.CTkButton(master=self.option_frame, text="무작위 초동 옵션", text_font=("맑은 고딕", 11), fg_color='grey80', hover_color='grey50', width=140, height=35, state=tkinter.DISABLED)
        self.random_init.grid(row=5, column=3)

        self.advanced = ctk.CTkButton(master=self.option_frame, text="고급 옵션", text_font=("맑은 고딕", 11), fg_color='grey80', hover_color='grey50', width=140, height=35, state=tkinter.DISABLED)
        self.advanced.grid(row=5, column=5)
        #=============================================

        self.okay_btn = ctk.CTkButton(master=self, text="계산", text_font=("맑은 고딕", 11), width=130, height=40, command=self.calc_prob)
        self.okay_btn.grid(row=3, column=1, sticky='w', padx=20, pady=15)

        self.cancel_btn = ctk.CTkButton(master=self, text="취소", text_font=("맑은 고딕", 11), fg_color='grey80', hover_color='grey50', width=130, height=40, command=self.close_win)
        self.cancel_btn.grid(row=3, column=3, sticky='e', padx=20, pady=15)

    def add_custom(self):
        window = add_custom(self)
        window.grab_set()

    def delete_custom(self):
        window = delete_custom(self)
        window.grab_set()

    def calc_prob(self):
        window = calculate(self)
        window.grab_set()

    def refresh_list(self, customs=[]):
        self.names_list=[]
        for items in self.parent.my_inits.init_list:
            self.names_list.append(items[1])
        self.names_list+=customs
        if len(self.names_list) >=2 : self.names_list.append("전체 확률")

        self.checklist_canvas.grid_remove()
        self.canvas_scrollbar.grid_remove()

        self.checklist_canvas = ctk.CTkCanvas(master=self.res_frame, background='white', height=150, bg='#DEDEDE')
        self.checklist_canvas.grid(row=0, column=0, sticky='nswe')

        self.canvas_scrollbar = ctk.CTkScrollbar(master=self.res_frame, orientation='vertical', height=150, command=self.checklist_canvas.yview)
        self.canvas_scrollbar.grid(row=0, column=1, sticky='nse')

        self.checklist_canvas.bind('<Configure>', lambda e: self.checklist_canvas.configure(scrollregion = self.checklist_canvas.bbox('all')))

        self.canvasframe = ctk.CTkFrame(master=self.checklist_canvas, corner_radius=0)
        self.canvasframe.grid_columnconfigure(0, weight=1)

        self.checklist_canvas.configure(yscrollcommand=self.canvas_scrollbar.set)
        self.checklist_canvas.create_window((0,0), window=self.canvasframe, width=500, anchor='nw')

        self.boxes = ChecklistBox(self.canvasframe, self.names_list, select=1)

    def custom_to_string(self):
        string_list=[]
        for custom in self.customs:
            if custom[0] == 1 : a = "AND : "
            else: a = "OR : "
            for idx in custom[1]:
                a+=(self.parent.my_inits.init_list[idx][1]+", ")
            a = a.rstrip(", ")
            string_list.append(a)
        return(string_list)

    def close_win(self): self.destroy()


class add_custom(ctk.CTkToplevel):
    
    WIDTH = 450
    HEIGHT = 500

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Add Custom")
        A = int(self.winfo_screenwidth()/2 - add_custom.WIDTH/2)
        B = int(self.winfo_screenheight()/2 - add_custom.HEIGHT/2)
        self.geometry(f"{add_custom.WIDTH}x{add_custom.HEIGHT}+{A}+{B}")
        self.iconbitmap("Galatea.ico")   # icon
        self.resizable(False, False)
        self.transient(parent)

        # configure grid layout (6x8)        
        self.grid_rowconfigure((1,3), minsize=20)
        self.grid_rowconfigure((5,7), minsize=10)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure((0,5), minsize=20)
        self.grid_columnconfigure(2, weight=1)

        self.notice_frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.notice_frame.grid(row=0, column=0, columnspan=6)

        self.notice = ctk.CTkLabel(master=self.notice_frame, text="AND/OR로 묶을 초동을 선택해주세요. (최소 2개)", text_font=("맑은 고딕", 11), height=60, width=self.WIDTH)
        self.notice.grid(row=0, column=0, columnspan=3, sticky='nswe')

        self.option_frame = ctk.CTkFrame(master=self)
        self.option_frame.grid(row=2, column=1, columnspan=4, sticky='nswe')

        self.option_frame.grid_columnconfigure((1,2), weight=1)
        self.option_frame.grid_columnconfigure(3, minsize=20)
        self.label_1 = ctk.CTkLabel(master=self.option_frame, text="옵션", width=120, text_font=("맑은 고딕", 11, 'bold'))
        self.label_1.grid(row=0, column=0)

        self.radvar = tkinter.IntVar(value=0)
        self.radio_1 = ctk.CTkRadioButton(master=self.option_frame, text_font=("맑은 고딕", 11), text="AND", variable = self.radvar, value=1)
        self.radio_1.grid(row=0, column=1, sticky='nswe', pady=5)
        self.radio_2 = ctk.CTkRadioButton(master=self.option_frame, text_font=("맑은 고딕", 11), text="OR", variable = self.radvar, value=0)
        self.radio_2.grid(row=0, column=2, sticky='nswe', pady=5)
        

        self.checklist_canvas = ctk.CTkCanvas(master=self, background='white', height=200, bg='#DEDEDE')
        self.checklist_canvas.grid(row=4, column=1, columnspan=3, sticky='nswe')

        self.canvas_scrollbar = ctk.CTkScrollbar(master=self, orientation='vertical', command=self.checklist_canvas.yview)
        self.canvas_scrollbar.grid(row=4, column=4, sticky='nse')

        self.checklist_canvas.bind('<Configure>', lambda e: self.checklist_canvas.configure(scrollregion = self.checklist_canvas.bbox('all')))

        self.canvasframe = ctk.CTkFrame(master=self.checklist_canvas, corner_radius=0)
        self.canvasframe.grid_columnconfigure(0, weight=1)

        self.checklist_canvas.configure(yscrollcommand=self.canvas_scrollbar.set)
        self.checklist_canvas.create_window((0,0), window=self.canvasframe, width=380, anchor='nw')

        init_list=[]
        for data in self.parent.parent.my_inits.init_list:
            init_list.append(data[1])

        self.boxes = ChecklistBox(self.canvasframe, init_list)

        self.okay_btn = ctk.CTkButton(master=self, text="확인", text_font=("맑은 고딕", 11), width=130, command=self.add_custom)
        self.okay_btn.grid(row=6, column=1, sticky='nsw')

        self.cancel_btn = ctk.CTkButton(master=self, text="취소", text_font=("맑은 고딕", 11), fg_color='grey80', hover_color='grey50', width=130, command=self.close_win)
        self.cancel_btn.grid(row=6, column=3, sticky='nse', columnspan=2)

    def add_custom(self):
        if len(self.boxes.getCheckedIdx()) <= 1 : pass
        self.parent.customs.append([self.radvar.get(), self.boxes.getCheckedIdx()])
        self.parent.refresh_list(customs=self.parent.custom_to_string())
        self.destroy()

    def close_win(self): self.destroy()


class delete_custom(ctk.CTkToplevel):
        
    WIDTH = 450
    HEIGHT = 400

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Delete Custom")
        A = int(self.winfo_screenwidth()/2 - delete_custom.WIDTH/2)
        B = int(self.winfo_screenheight()/2 - delete_custom.HEIGHT/2)
        self.geometry(f"{delete_custom.WIDTH}x{delete_custom.HEIGHT}+{A}+{B}")
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

        self.notice = ctk.CTkLabel(master=self.notice_frame, text="삭제할 내용을 선택하고 삭제 버튼을 눌러주세요.", text_font=("맑은 고딕", 11), height=60, width=self.WIDTH)
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

        self.custom_list=[]
        for data in self.parent.custom_to_string():
            self.custom_list.append(data)

        self.boxes = ChecklistBox(self.canvasframe, self.custom_list)

        self.okay_btn = ctk.CTkButton(master=self, text="삭제", text_font=("맑은 고딕", 11), width=130, height=40, command=self.delete_custom)
        self.okay_btn.grid(row=4, column=1, sticky='nsw')

        self.cancel_btn = ctk.CTkButton(master=self, text="취소", text_font=("맑은 고딕", 11), fg_color='grey80', hover_color='grey50', width=130, height=40, command=self.close_win)
        self.cancel_btn.grid(row=4, column=3, sticky='nse', columnspan=2)

    def delete_custom(self):
        indices = [i for i in range(len(self.custom_list)) if not i in self.boxes.getCheckedIdx()]
        new_customs = []
        for idx in indices: new_customs.append(self.parent.customs[idx])
        self.parent.customs = new_customs
        self.parent.refresh_list(customs=self.parent.custom_to_string())
        self.destroy()

    def close_win(self): self.destroy()



class calculate(ctk.CTkToplevel):
        
    WIDTH = 450
    HEIGHT = 450

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Calculating...")
        A = int(self.winfo_screenwidth()/2 - calculate.WIDTH/2)
        B = int(self.winfo_screenheight()/2 - calculate.HEIGHT/2)
        self.geometry(f"{calculate.WIDTH}x{calculate.HEIGHT}+{A}+{B}")
        self.iconbitmap("Galatea.ico")   # icon
        self.resizable(False, False)
        self.transient(parent)

        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)

        self.tbox = ctk.CTkTextbox(master=self, text_font=("맑은 고딕", 11))
        self.tbox.grid(row=0, column=0, sticky='nswe', padx=40, pady=40)

        self.tbox.insert('current', "계산중...\n\n")

        my_deck = self.parent.parent.my_deck                    # deck : .cards - list of (card name, # of card)
        
        idx_to_num = {str(k):v for k,v in my_deck.get_idx_to_num_dict().items()}

        my_init_list = [data[0] for data in self.parent.parent.my_inits.init_list]    # init_list :   list of [inits, name, result, tot]
        my_customs = self.parent.customs + [[0, list(range(len(my_init_list)))]]

        fstsnd = self.parent.first_second_var.get()
        if fstsnd[0] == "선" : draw_cards = 5
        else: draw_cards = 6

        useful_cards = set()

        for data in my_init_list:               # data : list of [[indices], nums, permisson]
            for mini_data in data:              # mini_data : [[indices], nums, permisson]
                for card_idx in mini_data[0]:   # card_idx : items of [indices]
                    useful_cards.add(card_idx)

        useful_cards = list(useful_cards)
        
        useful_cards_w_dup = []
        for idx in useful_cards:
            useful_cards_w_dup+= [idx] * my_deck.cards[idx][1]
        
        num_useless_cards = my_deck.num_cards - len(useful_cards_w_dup)

        # make all possible idx pairs for each init
        init_pair_list = []
        for init in my_init_list:
            init_pair = []
            for data in init:
                if data[2] == 0:        # duplication disallowed
                    init_pair.append(list(combinations(data[0], data[1])))      # append list of tuples
                else:
                    init_pair.append(list(combinations_with_replacement(data[0], data[1])))

            init_pair_list.append(list(product(*init_pair)))

        init_pair_set_list = []
        for init_pair in init_pair_list:
            init_pair_set=set()
            for tp in init_pair:
                a=[]
                for small_tp in tp:
                    for idx in small_tp:
                        a.append(idx)
                a.sort()
                init_pair_set.add(".".join([str(x) for x in a]))
            init_pair_set_list.append(init_pair_set)

        def duplicates(card_string):
            dup=1
            a = dict()
            for idx in card_string.split("."):
                if idx in a: a[idx]+=1
                else: a[idx]=1
            for card_idx in a:
                dup*=combinations_count(idx_to_num[card_idx], a[card_idx]) 
            return dup

        tot = combinations_count(my_deck.num_cards, draw_cards)
        answer_list = [0]*len(my_init_list)
        custom_answer_list = [0]*len(my_customs)

        for num_useful_cards in range(1,draw_cards+1):
            possible_cases = set(combinations([str(x) for x in useful_cards_w_dup], num_useful_cards))
            for tp in possible_cases:                               # for every possible useful card pairs
                cards = ".".join(tp)
                init_okay = [False]*len(init_pair_set_list)
                for idx in range(len(init_pair_set_list)):          # for every inits
                    for substring in init_pair_set_list[idx]:       # for every substring in one init
                        if isSubsequence(s=substring, t=cards):
                            init_okay[idx] = True
                            answer_list[idx] += duplicates(cards) * combinations_count(num_useless_cards, draw_cards-num_useful_cards)
                            break                                   # if any substring is suitable, stop for that inits

                for custom_idx in range(len(my_customs)):
                    b = (my_customs[custom_idx][0] == 0)
                    if b:       # OR mode
                        temp = False
                        for idx in my_customs[custom_idx][1]:   temp = temp or init_okay[idx]
                    
                    else:
                        temp = True
                        for idx in my_customs[custom_idx][1]:   temp = temp and init_okay[idx]

                    if temp: custom_answer_list[custom_idx] += duplicates(cards) * combinations_count(num_useless_cards, draw_cards-num_useful_cards)

        [data[1] for data in self.parent.parent.my_inits.init_list]

        for i in range(len(answer_list)):
            name = self.parent.parent.my_inits.init_list[i][1]
            self.tbox.insert('current', name+" : "+"{:.2f}".format(answer_list[i]/tot*100)+"%\n\n")

        self.tbox.insert('current', "===================\n\n")

        for i in range(len(custom_answer_list)-1):
            if my_customs[i][0] == 1: name = "AND : "
            else: name = "OR : "
            for idx in my_customs[i][1]:
                name += (self.parent.parent.my_inits.init_list[idx][1] + ", ")
            name = name[:len(name)-2]
            self.tbox.insert('current', name+" : "+"{:.2f}".format(custom_answer_list[i]/tot*100)+"%\n\n")
        
        if len(custom_answer_list) >1 : self.tbox.insert('current', "===================\n\n")
        self.tbox.insert('current', "전체 초동 확률 : "+"{:.2f}".format(custom_answer_list[-1]/tot*100)+"%")