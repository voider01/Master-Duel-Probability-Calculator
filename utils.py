import tkinter
import customtkinter as ctk
from operator import mul
from functools import reduce

class deck():
    def __init__(self):
        self.cards = []            # list of (card name, # of card)
        self.num_cards = 0
        self.valid_deck = self.valid     # valid deck : 40 <= num_cards <= 60, each 1<= # of card <=3
    
    def add_card(self, name, num_input):
        num = int(num_input)
        if num<=0 or num>=4 : pass  # print("not valid input")
        self.cards.append((name, num))
        self.num_cards += num
    
    def clear(self):
        self.cards=[]
        self.num_cards=0

    def valid(self):
        if self.num_cards<40 or self.num_cards>60: self.valid_deck = False
        else: self.valid_deck = True

    def __iter__(self):
        return iter(self.cards)

    def get_name_to_idx_dict(self):
        d = dict()
        cnt=0
        for card in self.cards:
            d[card[0]]=cnt
            cnt+=1
        return d

    def get_idx_to_num_dict(self):
        d=dict()
        cnt=0
        for card in self.cards:
            d[cnt]=card[1]
            cnt+=1
        return d

class groups():
    def __init__(self):
        self.group_list=[]

    def add(self, name, indices):
        self.group_list.append([name, indices])
    
    def get_name_to_idx_dict(self):
        d = dict()
        for group in self.group_list:
            d[group[0]]=group[1]
        return d

    def __iter__(self):
        return iter(self.group_list)

class inits():
    def __init__(self):
        self.init_list=[]
        self.init_string_list=[]
    
    def add(self, inits, inits_string, name, result, tot):
        self.init_list.append([inits, name, result, tot])
        self.init_string_list.append([inits_string, name, result, tot])

    def edit(self, idx, inits, inits_string, name, result, tot):
        self.init_list[idx]=[inits, name, result, tot]
        self.init_string_list[idx]=[inits_string, name, result, tot]

    def get_name_to_string_list_dict(self):
        d = dict()
        for a in self.init_string_list:
            d[a[1]]=a
        return d

    def get_name_to_idx_dict(self):
        d = dict()
        cnt=0
        for a in self.init_string_list:
            d[a[1]]=cnt
            cnt+=1
        return d


class ChecklistBox(ctk.CTkFrame):
    def __init__(self, parent, choices, select=0, **kwargs):
        ctk.CTkFrame.__init__(self, parent, **kwargs)

        self.vars = []
        self.boxes = []

        cnt=0
        bg = self.cget("background")
        for choice in choices:
            var = ctk.StringVar(value=choice)
            self.vars.append(var)
            cb = ctk.CTkCheckBox(master=parent, variable=var, text=choice,
                                onvalue=cnt, offvalue=-1,
                                background=bg,
                                text_font=("맑은 고딕", 10, 'bold'))
            cb.grid(row=cnt, column=0, padx=10, pady=8, sticky='nsw')
            if select==0: cb.deselect()
            else:cb.select()
            self.boxes.append(cb)
            cnt+=1

    def getCheckedIdx(self):
        values = []
        for var in self.vars:
            value = var.get()
            if value != '-1':
                values.append(int(value))
        return values

    def checkwithidx(self, indices):
        for cb in self.boxes:
            cb.deselect()
        
        for idx in indices:
            self.boxes[idx].select()

    def remove(self):
        for cb in self.boxes: cb.grid_remove()

def combinations_count(n, r):
    r = min(r, n - r)
    numer = reduce(mul, range(n, n - r, -1), 1)
    denom = reduce(mul, range(1, r + 1), 1)
    return numer // denom


def isSub(s, t):
    # s : sub, list of idx
    # t : cards, tuple of idx

    len_s = len(s)
    len_t = len(t)
    if len_s > len_t : return False
    
    cnt = 0
    for val in t:
        if val == s[cnt]:
            cnt = cnt + 1
            
            if cnt == len_s:
                return True
            
    return False