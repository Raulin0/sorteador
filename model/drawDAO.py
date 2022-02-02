import json
import os
from datetime import datetime


class drawDAO:
    @classmethod
    def save_draw(cls, draw):
        obj = {}
        obj[f"{datetime.now().strftime('%d/%m/%Y %H:%M')}"] = draw

        path = 'draws/'

        if not os.path.exists(path):
            os.makedirs(path)

        base_dir = os.path.dirname(path)
        save_to = os.path.join(base_dir, 'sorteios.json')

        try:
            with open(save_to, 'r', encoding='utf-8') as s:
                draw_list = json.load(s)
        except:
            draw_list = []

        draw_list.append(obj)

        with open(save_to, 'w', encoding='utf-8') as f:
            js = json.dumps(draw_list, indent=4, ensure_ascii=False)
            f.write(js)
        print(cls.print_log(f'Sorteio salvo em {save_to}'))
