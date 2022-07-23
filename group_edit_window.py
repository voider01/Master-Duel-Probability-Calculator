import tkinter
import customtkinter as ctk
from utils import *

class group_edit_window(ctk.CTkToplevel):
    
    WIDTH = 600
    HEIGHT = 600

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Group Edit")
        A = int(self.winfo_screenwidth()/2 - group_edit_window.WIDTH/2)
        B = int(self.winfo_screenheight()/2 - group_edit_window.HEIGHT/2)
        self.geometry(f"{group_edit_window.WIDTH}x{group_edit_window.HEIGHT}+{A}+{B}")
        self.iconbitmap("Galatea.ico")   # icon
        self.resizable(False, False)
        self.transient(parent)           # only use parent window

        self.groups=groups()

        # ============ create one frame ============        

        # configure grid layout (3x7)
        self.grid_rowconfigure(1, minsize=30)
        self.grid_rowconfigure((2, 3, 4, 5, 6), weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, minsize=20)

        self.notice_frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.notice_frame.grid(row=0, column=0, columnspan=3)

        self.notice = ctk.CTkLabel(master=self.notice_frame,
                                                   text="초동에 사용되는 특정 카드들을 묶어 카드군으로 만들 수 있습니다.\n"
                                                   +"예를 들어, 프랭키즈 덱의 초동인 '프랭키즈 하급' 몬스터를\n 카드군으로 묶을 수 있습니다.\n\n"
                                                   +"'반드시' 카드군 이름을 덱에 들어간 카드 이름과 다르게 해 주세요.",
                                                   text_font=("맑은 고딕", 11),
                                                   width=group_edit_window.WIDTH,
                                                   height = 140,
                                                   anchor=tkinter.CENTER,
                                                   justify=tkinter.CENTER)
        self.notice.pack()

        self.group_frame = ctk.CTkFrame(master=self)
        self.group_frame.grid(row=2,column=0,rowspan=5,sticky='nswe', padx=20, pady=20)
        # configure grid layout (2x1)
        self.group_frame.grid_columnconfigure(0, weight=1)
        self.group_frame.grid_rowconfigure(0, weight=1)

        self.group_list_scrollbar = ctk.CTkScrollbar(master=self.group_frame)
        self.group_list = ctk.CTkTextbox(master=self.group_frame, text_font=("맑은 고딕", 12), yscrollcommand=self.group_list_scrollbar.set, state=tkinter.DISABLED)
        self.group_list.grid(row=0, column=0, sticky='nswe', padx=20, pady=20)
        
        self.group_list_scrollbar.grid(row=0, column=1, sticky='nswe', pady=20)
        self.group_list_scrollbar.configure(command=self.group_list.yview)

        self.load_groups()
        self.refresh_group()

        self.add_group_btn = ctk.CTkButton(master=self, text="카드군 추가", text_font=("맑은 고딕", 11), height=40, fg_color='grey80', hover_color='grey50', command=self.add_group)
        self.add_group_btn.grid(row=2, column=1)

        self.edit_group_btn = ctk.CTkButton(master=self, text="카드군 수정", text_font=("맑은 고딕", 11), height=40, fg_color='grey80', hover_color='grey50', command=self.edit_group)
        self.edit_group_btn.grid(row=3, column=1)

        self.delete_group_btn = ctk.CTkButton(master=self, text="카드군 삭제", text_font=("맑은 고딕", 11), height=40, fg_color='grey80', hover_color='grey50', command=self.delete_group)
        self.delete_group_btn.grid(row=4, column=1)

        self.okay_btn = ctk.CTkButton(master=self, text="확인", text_font=("맑은 고딕", 11), height=40, command=self.save_groups)
        self.okay_btn.grid(row=5, column=1)

        self.cancel_btn = ctk.CTkButton(master=self, text="취소", text_font=("맑은 고딕", 11), height=40, fg_color='grey80', hover_color='grey50', command=self.close_win)
        self.cancel_btn.grid(row=6, column=1)
        
    def add_group(self):
        window = add_group(self)
        window.grab_set()

    def edit_group(self):
        window = edit_group(self)
        window.grab_set()
    
    def delete_group(self):
        window = delete_group(self)
        window.grab_set()

    def save_groups(self):
        self.parent.my_group = self.groups
        self.destroy()

    def load_groups(self):
        self.groups = self.parent.my_group

    def close_win(self): self.destroy()

    def refresh_group(self):
        self.group_list.configure(state=tkinter.NORMAL)
        self.group_list.delete(0.0, "end")
        cnt=1
        for items in self.groups:
            self.group_list.insert("current", f"{cnt}. "+str(items[0])+ f": {len(items[1])}종류\n")
            cnt+=1
        self.group_list.delete("end-2c", "end")
        self.group_list.configure(state=tkinter.DISABLED)

        
        
class add_group(ctk.CTkToplevel):

    WIDTH = 450
    HEIGHT = 500

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Add Group")
        A = int(self.winfo_screenwidth()/2 - add_group.WIDTH/2)
        B = int(self.winfo_screenheight()/2 - add_group.HEIGHT/2)
        self.geometry(f"{add_group.WIDTH}x{add_group.HEIGHT}+{A}+{B}")
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

        self.notice = ctk.CTkLabel(master=self.notice_frame, text="카드군에 추가할 카드를 선택하고 확인 버튼을 눌러주세요.", text_font=("맑은 고딕", 11), height=60, width=self.WIDTH)
        self.notice.grid(row=0, column=0, columnspan=3, sticky='nswe')

        self.name_frame = ctk.CTkFrame(master=self)
        self.name_frame.grid(row=2, column=1, columnspan=4, sticky='nswe')

        self.name_frame.grid_columnconfigure(1, weight=1)
        self.name_frame.grid_columnconfigure(2, minsize=20)
        self.label_1 = ctk.CTkLabel(master=self.name_frame, text="이름", width=120, text_font=("맑은 고딕", 11, 'bold'))
        self.label_1.grid(row=0, column=0)

        self.group_name = ctk.CTkEntry(master=self.name_frame, text_font=("맑은 고딕", 11), placeholder_text="카드군 이름")
        self.group_name.grid(row=0, column=1, sticky='nswe', pady=5)

        self.checklist_canvas = ctk.CTkCanvas(master=self, background='white', height=200, bg='#DEDEDE')
        self.checklist_canvas.grid(row=4, column=1, columnspan=3, sticky='nswe')

        self.canvas_scrollbar = ctk.CTkScrollbar(master=self, orientation='vertical', command=self.checklist_canvas.yview)
        self.canvas_scrollbar.grid(row=4, column=4, sticky='nse')

        self.checklist_canvas.bind('<Configure>', lambda e: self.checklist_canvas.configure(scrollregion = self.checklist_canvas.bbox('all')))

        self.canvasframe = ctk.CTkFrame(master=self.checklist_canvas, corner_radius=0)
        self.canvasframe.grid_columnconfigure(0, weight=1)

        self.checklist_canvas.configure(yscrollcommand=self.canvas_scrollbar.set)
        self.checklist_canvas.create_window((0,0), window=self.canvasframe, width=380, anchor='nw')

        self.checklist_canvas.pack_propagate(0)

        card_list=[]
        for data in self.parent.parent.my_deck:
            card_list.append(data[0])

        self.boxes = ChecklistBox(self.canvasframe, card_list)

        self.okay_btn = ctk.CTkButton(master=self, text="확인", text_font=("맑은 고딕", 11), width=130, command=self.add_group)
        self.okay_btn.grid(row=6, column=1, sticky='nsw')

        self.cancel_btn = ctk.CTkButton(master=self, text="취소", text_font=("맑은 고딕", 11), fg_color='grey80', hover_color='grey50', width=130, command=self.close_win)
        self.cancel_btn.grid(row=6, column=3, sticky='nse', columnspan=2)

    def add_group(self):
        if len(self.boxes.getCheckedIdx()) != 0:
            self.parent.groups.add(self.group_name.get(), self.boxes.getCheckedIdx())
            self.parent.refresh_group()
        self.destroy()

    def close_win(self): self.destroy()



class edit_group(ctk.CTkToplevel):
    
    WIDTH = 450
    HEIGHT = 500

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Edit Group")
        A = int(self.winfo_screenwidth()/2 - edit_group.WIDTH/2)
        B = int(self.winfo_screenheight()/2 - edit_group.HEIGHT/2)
        self.geometry(f"{edit_group.WIDTH}x{edit_group.HEIGHT}+{A}+{B}")
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

        self.notice = ctk.CTkLabel(master=self.notice_frame, text="카드군 이름을 선택하고 수정한 뒤 확인 버튼을 눌러주세요.", text_font=("맑은 고딕", 11), height=60, width=self.WIDTH)
        self.notice.grid(row=0, column=0, columnspan=3, sticky='nswe')

        self.name_frame = ctk.CTkFrame(master=self)
        self.name_frame.grid(row=2, column=1, columnspan=4, sticky='nswe')

        self.name_frame.grid_columnconfigure(1, weight=1)
        self.name_frame.grid_columnconfigure(2, minsize=20)
        self.label_1 = ctk.CTkLabel(master=self.name_frame, text="이름", width=120, text_font=("맑은 고딕", 11, 'bold'))
        self.label_1.grid(row=0, column=0)

        group_names = [a[0] + f": {len(a[1])}종류" for a in self.parent.groups]

        var = tkinter.StringVar(value="카드군 이름")
        self.group_name = ctk.CTkOptionMenu(master=self.name_frame, values = group_names, variable=var, text_font=("맑은 고딕", 10), dropdown_text_font=("맑은 고딕", 10), fg_color='white', button_color='grey60', command=self.load_group)
        self.group_name.grid(row=0, column=1, sticky='nswe', pady=5)

        self.checklist_canvas = ctk.CTkCanvas(master=self, background='white', height=200, bg='#DEDEDE')
        self.checklist_canvas.grid(row=4, column=1, columnspan=3, sticky='nswe')

        self.canvas_scrollbar = ctk.CTkScrollbar(master=self, orientation='vertical', command=self.checklist_canvas.yview)
        self.canvas_scrollbar.grid(row=4, column=4, sticky='nse')

        self.checklist_canvas.bind('<Configure>', lambda e: self.checklist_canvas.configure(scrollregion = self.checklist_canvas.bbox('all')))

        self.canvasframe = ctk.CTkFrame(master=self.checklist_canvas, corner_radius=0)
        self.canvasframe.grid_columnconfigure(0, weight=1)

        self.checklist_canvas.configure(yscrollcommand=self.canvas_scrollbar.set)
        self.checklist_canvas.create_window((0,0), window=self.canvasframe, width=380, anchor='nw')

        card_list=[]
        for data in self.parent.parent.my_deck:
            card_list.append(data[0])

        self.boxes = ChecklistBox(self.canvasframe, card_list)

        self.okay_btn = ctk.CTkButton(master=self, text="확인", text_font=("맑은 고딕", 11), width=130, command=self.edit_group)
        self.okay_btn.grid(row=6, column=1, sticky='nsw')

        self.cancel_btn = ctk.CTkButton(master=self, text="취소", text_font=("맑은 고딕", 11), fg_color='grey80', hover_color='grey50', width=130, command=self.close_win)
        self.cancel_btn.grid(row=6, column=3, sticky='nse', columnspan=2)

    def load_group(self, name):
        for group in self.parent.groups:
            if name.split(":")[0] == group[0]: self.boxes.checkwithidx(group[1])

    def edit_group(self):
        name=self.group_name.get()
        if name == "카드군 이름" : pass
        else :
            for group in self.parent.groups:
                if name.split(":")[0] == group[0]:
                    group[1]=self.boxes.getCheckedIdx()
                    break
        self.parent.refresh_group()
        self.destroy()

    def close_win(self): self.destroy()


class delete_group(ctk.CTkToplevel):
        
    WIDTH = 450
    HEIGHT = 400

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Delete Group")
        A = int(self.winfo_screenwidth()/2 - delete_group.WIDTH/2)
        B = int(self.winfo_screenheight()/2 - delete_group.HEIGHT/2)
        self.geometry(f"{delete_group.WIDTH}x{delete_group.HEIGHT}+{A}+{B}")
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

        self.notice = ctk.CTkLabel(master=self.notice_frame, text="삭제할 카드군을 선택하고 삭제 버튼을 눌러주세요.", text_font=("맑은 고딕", 11), height=60, width=self.WIDTH)
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

        self.group_list=[]
        for data in self.parent.groups:
            self.group_list.append(data[0])

        self.boxes = ChecklistBox(self.canvasframe, self.group_list)

        self.okay_btn = ctk.CTkButton(master=self, text="삭제", text_font=("맑은 고딕", 11), width=130, height=40, command=self.delete_group)
        self.okay_btn.grid(row=4, column=1, sticky='nsw')

        self.cancel_btn = ctk.CTkButton(master=self, text="취소", text_font=("맑은 고딕", 11), fg_color='grey80', hover_color='grey50', width=130, height=40, command=self.close_win)
        self.cancel_btn.grid(row=4, column=3, sticky='nse', columnspan=2)

    def delete_group(self):
        indices = [i for i in range(len(self.group_list)) if not i in self.boxes.getCheckedIdx()]
        new_groups = []
        for idx in indices: new_groups.append(self.parent.groups.group_list[idx])
        self.parent.groups.group_list = new_groups

        self.parent.refresh_group()
        self.destroy()

    def close_win(self): self.destroy()