import os
import random

from bs4 import BeautifulSoup


class WishMaker:
    """
    Makes wishes from local file and joins it with list of birthdays
    """
    def __init__(self):
        try:
            self.wishes = list()
            congrats = os.path.join(os.path.dirname(__file__), 'congrats.html')
            with open(congrats, 'r', encoding='utf-8') as html_doc:
                soup = BeautifulSoup(html_doc, 'html.parser')
                p_list = soup.find_all('p')
                for p in p_list:
                    self.wishes.append(p.get_text())
        except FileNotFoundError:
            self.wishes = ['Желаю здоровья, счастья, а также успехов на работе и в личной жизни.']

    def make_wish(self, whom):
        n = len(whom)
        start = str()
        guys = str()
        wish = random.choice(self.wishes)
        end = random.choice(['\n\nНакидайте стикеросов!',
                             '\n\nВыпускайте собак!',
                             '\n\nКидайте собак!'])
        if n == 1:
            name = whom[0][0]
            tg = whom[0][1]
            start = f'Сегодня днюху празднует '
            guys = f'🧁 {name} ({tg})!'
        elif n > 1:
            start = 'Сегодня празднуют ДР:\n'
            guys_list = list()
            for i in range(len(whom)):
                name = whom[i][0]
                tg = whom[i][1]
                guys_list.append(f'🎂 {name} ({tg})')
            guys = '\n'.join(guys_list)

        if len(guys) > 0:
            wish = start + guys + '\n\n' + wish + end
            return wish
