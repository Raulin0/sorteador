# **SORTEADOR PONTO PY**
	
## **Introdução**

Realize sorteios, sem repetições de sorteados, através da importação de um arquivo **.txt** contendo os nomes e posteriormente salvando cada um dos sorteios realizados, com a data e horario da sua realização, em um arquivo **.json**.

<div align='center'>
	<p>
		<img src='https://user-images.githubusercontent.com/17261167/151827289-e08a0ad9-1600-4943-8017-decd63ea0f09.png' width='410'>
		<img src='https://user-images.githubusercontent.com/17261167/152173731-23cc064b-8e41-49b9-ad02-cb653fc2984c.gif' width='410'>
	</p>
</div>

## **Tecnologias**

Para desenvolvermos esse projeto utilizamos a linguagem:

<div align="center">
	<p>
		<a href='https://www.python.org'>
			<img src='https://user-images.githubusercontent.com/17261167/148867507-ba2bc362-3d9a-4e7b-808d-d27709f2e242.png' height='150'>
		</a>
	</p>
</div>

Especificamente as bibliotecas:

* **Tkinter** - Permite desenvolver a interface gráfica;
* **Random** - Utilizado para embaralhar a lista de nomes e realizar o sorteio;
* **Datetime** - Responsável por capturar a data e horário do sorteio;
* **Json** - Utilizado para salvar todos os sorteios realizados (nomes e sorteados) em um arquivo .json com as datas e horarios de cada sorteio
* **Os** - Responsável por criar o caminho da pasta onde será salvo o arquivo.json contendo todos os sorteios

## **Requisitos**

* Ter instalado Python na versão 3.10 (o desenvolvimento do projeto foi realizado na versão 3.10, então não garantimos o funcionamento da aplicação em versões anteriores);
* Ter um arquivo .txt contendo os nomes que serão objeto do sorteio (podendo conter qualquer tipo e quantidade de nomes para a realização, contanto que seja um por linha).

**Exemplo**:

```
Marcos
Felipe
Mario
Matheus
Francisco
Antonio
Eduarda
Maria
José
Murilo
Miguel
Daniela
...
```

## **Realizando um sorteio**

Executado o arquivo **main**, será inicializada a interface gráfica da aplicação facilitando a navegação e inserção das informações necessárias para realizar o sorteio.

```py
from view.view import View

if __name__ == '__main__':
    app = View()
```

O usuário deve seguir os seguintes passos:

### 1 - Importando nomes

Clicando no botão **"carregar nomes"**, uma aba de seleção surgirá, na qual o usuário deverá **selecionar o arquivo .txt** contendo os nomes que serão objeto do sorteio (um por linha, conforme o exemplo acima). Assim o programa irá, através de **list comprehension**, importar linha por linha, adicionando os nomes em uma lista que posteriormente será utilizada:

```py
    def load_names(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as names:
            self.draw['nomes'] = [name.strip() for name in names]
        print(self.print_log(
            f"Lista de nomes carregados - {self.draw['nomes']}"))
```

Ao passo que que serão exibidos na listbox da esquerda da interface gráfica, assim como um indicativo de quantos nomes foram carregados:

```py
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
```

### 2 - Inserindo quantos serão sorteados

No espaço de entrada, o usuário poderá digitar um número de 1 a 100, como entrada válida, que será utilizada posteriormente como parâmetro para determinar quantos participantes serão sorteados. As seguintes linhas de código são as responsáveis por permitir apenas a entrada de números inteiros de 1 a 100:

```py
class ValidateDraw:
    def validate_entry(self, num):
        if num == '':
            return True
        try:
            value = int(num)
        except ValueError:
            return False
        return 1 <= value <= 100

    def validate_command(self):
        self.vcmd = (self.root.register(self.validate_entry), '%P')
```

O número inserido, também, não pode ser superior a quantidade total de participantes que estiverem no sorteio (Ex: 12 nomes não poderão ser sorteados se somente 10 estiverem concorrendo).

### 3 - Sorteando

Após importar os nomes e inserir quantos deles serão sorteados basta clicar no botão **"sortear"** que o programa iniciará a **contagem regressiva** (desabilitando os botões até que a contagem termine, para evitar quaisquer conflitos) para gerar a lista de sorteados e adicionar os nomes na listbox à direita:

```py
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
```

Por fim, utilizará a biblioteca **random**, mais especificamente a função **sample**, duas vezes: na primeira, para embaralhar a lista de nomes; e na segunda gerar a lista de sorteados.

```py
    def generate_names(self):
        shuffled_names = sample(self.draw['nomes'], len(self.draw['nomes']))
        draft = sample(shuffled_names, int(self.entry_drawn_num.get()))

        self.draw['sorteados'] = draft

        print(self.print_log(
            f"Lista de nomes sorteados - {self.draw['sorteados']}"))

        self.save_draw(self.draw)
```

Exceto se ocorrer algum dos seguintes erros:

* **Erro por não ter importado participantes**:

<p align='center'>
  <img src='https://user-images.githubusercontent.com/17261167/151856033-ba4e732a-973f-4682-ab2f-f10edb138806.png' width='410'>
</p>

* **Erros na entrada de participantes a serem sorteados**:

<div align='center'>
  <p>
    <img src='https://user-images.githubusercontent.com/17261167/151856117-af4ae496-a3f4-431c-8d46-91afdbddd69a.png' width='410'>
    <img src='https://user-images.githubusercontent.com/17261167/151856193-afd389bd-cb2d-41a0-8afd-cd8cfe3dfd3a.png' width='410'>
  </p>
</div>

Realizadas as correções indicadas pelo programa, o sorteio será realizado e a listbox da direita será preenchida normalmente com os nomes sorteados.

### 4 - Salvando sorteios

Uma vez realizado o sorteio, o seguinte método será responsável por salvar o dicionário contendo o nomes carregados e os nomes sorteados para em segundo dicionário que cotém como chave a data e horario gerada pela biblioteca **datetime**:

```py
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
```

O sorteio que agora pode ser identificado com sua respectiva data e horário será salvo dentro de um array em um arquivo .json, que estará localizado na pasta **"draws"**, criada através da biblioteca "os".

**Exemplo**:

```json
[
    {
        "31/01/2022 16:56": {
            "Nomes": [
                "Marcos",
                "Felipe",
                "Mario",
                "Matheus",
                "Francisco",
                "Antonio",
                "Thiago",
                "Igor",
                "Paulo",
                "João",
                "Rafael",
                "Sarah"
            ],
            "Sorteados": [
                "Francisco",
                "Rafael",
                "Igor",
                "Sarah"
            ]
        }
    }
]
```

### 5 - Limpando sorteios

Para realizar a limpeza dos dados do sorteio, os seguintes métodos serão os responsáveis, ao pressionar o botão **"limpar sorteio"**:

```py
    def clear(self):
        self.clear_raffle()
        self.listbox_names.delete(0, 'end')
        self.listbox_drawn.delete(0, 'end')
        self.entry_drawn_num.delete(0, 'end')
        self.label_quant_loaded[
            'text'] = f"Quantidade de nomes carregados: {len(self.draw['nomes'])}"
```
```py
    def clear_raffle(self):
        self.draw['nomes'].clear()
        self.draw['sorteados'].clear()
        print(self.print_log('Sorteio limpo'))
```
