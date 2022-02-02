import tkinter as tk
from tkinter.filedialog import askopenfilename
from controller.raffle import Raffle
from controller.validate_draw import ValidateDraw


class View(Raffle, ValidateDraw):
    def __init__(self):
        super().__init__()
        self.create_view()

    def create_view(self):
        self.root = tk.Tk()
        self.create_window()
        self.create_frames()
        self.create_label()
        self.create_buttons()
        self.validate_command()
        self.create_entry()
        self.create_listbox()
        self.root.mainloop()

    def create_window(self):
        self.root.title('Sorteador Ponto Py')
        self.root.geometry('700x800+600+100')
        self.root.resizable(False, False)
        self.root.iconbitmap('images/sorteador_icon.ico')

    def create_frames(self):
        self.frame_logo = tk.Frame(self.root)
        self.frame_logo.pack()

        self.frame_raffle = tk.Frame(self.root)
        self.frame_raffle.pack()

        self.frame_raffle_text = tk.Frame(self.frame_raffle)
        self.frame_raffle_text.pack(side='left', padx=(0, 20))

        self.frame_entries = tk.Frame(self.frame_raffle)
        self.frame_entries.pack(side='right')

        self.frame_load_names = tk.Frame(self.frame_entries)
        self.frame_load_names.pack()

        self.frame_drawn_num = tk.Frame(self.frame_entries)
        self.frame_drawn_num.pack(side='left', pady=(10, 0))

        self.frame_btn_draw = tk.Frame(self.root)
        self.frame_btn_draw.pack(pady=25)

        self.frame_quant_loaded = tk.Frame(self.root)
        self.frame_quant_loaded.pack(pady=(0, 25))

        self.frame_listboxes = tk.Frame(self.root)
        self.frame_listboxes.pack()

        self.frame_listbox_names = tk.Frame(self.frame_listboxes)
        self.frame_listbox_names.pack(side='left', padx=(0, 10))

        self.frame_listbox_drawn = tk.Frame(self.frame_listboxes)
        self.frame_listbox_drawn.pack(side='right', padx=(10, 0))

        self.frame_btn_clear = tk.Frame(self.root)
        self.frame_btn_clear.pack(pady=25)

    def create_label(self):
        self.insert_logo()
        self.label_img_logo = tk.Label(self.frame_logo, image=self.img_logo)
        self.label_img_logo.pack(pady=(25, 50))

        self.label_raffle_load_text = tk.Label(
            self.frame_raffle_text, text='Selecione um arquivo .txt', font='Raleway 12 bold')
        self.label_raffle_load_text.pack()

        self.label_raffle_num_text = tk.Label(
            self.frame_raffle_text, text='Quantos serão sorteados?', font='Raleway 12 bold')
        self.label_raffle_num_text.pack(pady=(20, 0))

        self.label_instr_num_text = tk.Label(
            self.frame_drawn_num, text='(De 1 a 100)', font='Raleway 10')
        self.label_instr_num_text.pack(side='right', padx=10)

        self.label_quant_loaded = tk.Label(
            self.frame_quant_loaded, text=f"Quantidade de nomes carregados: {len(self.draw['nomes'])}", font='Raleway 12 bold')
        self.label_quant_loaded.pack()

    def insert_logo(self):
        self.img_logo = tk.PhotoImage(file='images/sorteador_logo.png')

    def create_buttons(self):
        self.btn_load_names = tk.Button(self.frame_load_names, text='Carregar nomes', command=lambda: self.search_names(),
                                        font='Raleway', bg='#3d85c6', fg='white', relief='flat', cursor='hand2')
        self.btn_load_names.pack()

        self.btn_draw = tk.Button(
            self.frame_btn_draw, text='Sortear', command=lambda: self.draft(), font='Raleway', bg='#3d85c6', fg='white', relief='flat', cursor='hand2')
        self.btn_draw.pack(ipadx=30)

        self.btn_clear = tk.Button(
            self.frame_btn_clear, text='Limpar sorteio', command=lambda: self.clear(), font='Raleway', bg='#DC143C', fg='white', relief='flat', cursor='hand2')
        self.btn_clear.pack()

    def create_entry(self):
        self.entry_drawn_num = tk.Entry(self.frame_drawn_num, validate='key', validatecommand=self.vcmd,
                                        font='Raleway 16', justify='center', width=3, relief='flat')
        self.entry_drawn_num.pack(side='left')

    def create_listbox(self):
        self.scrollbar_listbox_names = tk.Scrollbar(
            self.frame_listbox_names, relief='flat')
        self.scrollbar_listbox_names.pack(side='right', fill='y')
        self.listbox_names = tk.Listbox(self.frame_listbox_names, height=10,
                                        width=30, relief='flat', font='Raleway 10')
        self.listbox_names.config(
            yscrollcommand=self.scrollbar_listbox_names.set)
        self.scrollbar_listbox_names.config(
            command=self.listbox_names.yview)
        self.listbox_names.pack()

        self.scrollbar_listbox_drawn = tk.Scrollbar(
            self.frame_listbox_drawn, relief='flat')
        self.listbox_drawn = tk.Listbox(self.frame_listbox_drawn, height=10,
                                        width=30, relief='flat', font='Raleway 10')
        self.listbox_drawn.config(
            yscrollcommand=self.scrollbar_listbox_drawn.set)
        self.scrollbar_listbox_drawn.config(
            command=self.listbox_drawn.yview)
        self.scrollbar_listbox_drawn.pack(side='right', fill='y')
        self.listbox_drawn.pack()

    def search_names(self):
        file_path = askopenfilename(parent=self.root, title='Escolha um arquivo .txt', filetype=[
            ('Arquivo txt', '*.txt')])
        if file_path:
            self.listbox_names.delete(0, 'end')
            self.listbox_drawn.delete(0, 'end')
            self.load_names(file_path)
            self.label_quant_loaded[
                'text'] = f"Quantidade de nomes carregados: {len(self.draw['nomes'])}"
            for name in self.draw['nomes']:
                self.listbox_names.insert('end', name)

    def draft(self):
        error = {'1': 'Informe quantos participantes serão sorteados', '2': 'Carregue um arquivo .txt contendo os participantes',
                 '3': 'O espaço "Quantos serão sorteados?" precisa ser preenchido com um número menor ou igual a quantidade de participantes'}

        if self.draw['nomes'] == []:
            print(self.print_log(error['2']))
            tk.messagebox.showerror('Erro', error['2'])

        if self.entry_drawn_num.get() == '':
            print(self.print_log(error['1']))
            tk.messagebox.showerror('Erro', error['1'])

        elif len(self.draw['nomes']) < int(self.entry_drawn_num.get()):
            print(self.print_log(error['3']))
            tk.messagebox.showerror('Erro', error['3'])

        else:
            self.listbox_drawn.delete(0, 'end')
            self.btn_load_names['state'] = tk.DISABLED
            self.btn_draw['state'] = tk.DISABLED
            self.btn_clear['state'] = tk.DISABLED
            self.countdown(3)

    def countdown(self, count):
        self.label_quant_loaded['text'] = 'Contagem regressiva: {:02d}'.format(
            count)
        if count > 0:
            self.root.after(1000, self.countdown, count-1)
        if self.label_quant_loaded['text'] == 'Contagem regressiva: 00':
            self.generate_names()
            for drawn in self.draw['sorteados']:
                self.listbox_drawn.insert('end', drawn)
            self.btn_load_names['state'] = tk.NORMAL
            self.btn_draw['state'] = tk.NORMAL
            self.btn_clear['state'] = tk.NORMAL
            self.label_quant_loaded[
                'text'] = f"Quantidade de nomes carregados: {len(self.draw['nomes'])}"

    def clear(self):
        self.clear_raffle()
        self.listbox_names.delete(0, 'end')
        self.listbox_drawn.delete(0, 'end')
        self.entry_drawn_num.delete(0, 'end')
        self.label_quant_loaded[
            'text'] = f"Quantidade de nomes carregados: {len(self.draw['nomes'])}"
