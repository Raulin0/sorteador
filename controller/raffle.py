from random import sample
from controller.log import Log
from model.draw import Draw
from model.drawDAO import drawDAO


class Raffle(Draw, drawDAO, Log):
    def __init__(self):
        super().__init__()

    def load_names(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as names:
            self.draw['nomes'] = [name.strip() for name in names]
        print(self.print_log(
            f"Lista de nomes carregados - {self.draw['nomes']}"))

    def generate_names(self):
        shuffled_names = sample(self.draw['nomes'], len(self.draw['nomes']))
        draft = sample(shuffled_names, int(self.entry_drawn_num.get()))

        self.draw['sorteados'] = draft

        print(self.print_log(
            f"Lista de nomes sorteados - {self.draw['sorteados']}"))

        self.save_draw(self.draw)

    def clear_raffle(self):
        self.draw['nomes'].clear()
        self.draw['sorteados'].clear()
        print(self.print_log('Sorteio limpo'))
