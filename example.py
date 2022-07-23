        self.canvas = ctk.CTkCanvas(master=self.frame_right_1, bg='white', relief='flat')
        self.canvas.grid(row=0, column=0, sticky='nswe')

        self.canvas_scrollbar = ctk.CTkScrollbar(master=self.frame_right_1, orientation='vertical', command=self.canvas.yview)
        self.canvas_scrollbar.grid(row=0, column=1, sticky='ns')

        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox('all')))

        self.canvasframe = ctk.CTkFrame(master=self.canvas, corner_radius=0)
        self.canvasframe.grid_columnconfigure(0, weight=1)

        self.canvas.configure(yscrollcommand=self.canvas_scrollbar.set)
        self.canvas.create_window((0,0), window=self.canvasframe, width=565, anchor='nw')

        self.canvas.pack_propagate(0)


        for i in range(50):
            btn = ctk.CTkButton(master=self.canvasframe, text=f'my button {i+1}')
            btn.grid(row=i, column=0, sticky='ns', pady=20)