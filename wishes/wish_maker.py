import os
import random
import time

from balaboba import Balaboba
from bs4 import BeautifulSoup


class WishMaker:
    """
    Makes wishes by Balaboba with prompting from local file, then joins it with list of birthday guys
    """

    def __init__(self):
        # https://github.com/monosans/balaboba
        self.bb = Balaboba()
        intros = self.bb.intros(language='ru')
        self.intro = next(intros)

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

    @staticmethod
    def parse_one(who):
        name = who[0][0]
        tg = who[0][1]
        start = f'Сегодня днюху празднует '
        if name and tg:
            guys = f'🧁 {name} ({tg})!'
        elif not tg and name:
            guys = f'🧁 {name}!'
        else:
            guys = '😎 Человек без имени и телеги!'
        return start, guys

    @staticmethod
    def parse_many(who):
        start = 'Сегодня празднуют ДР:\n'
        guys_list = list()
        for i in range(len(who)):
            name = who[i][0]
            tg = who[i][1]
            if name and tg:
                guys_list.append(f'🎂 {name} ({tg})')
            elif not tg and name:
                guys_list.append(f'🎂 {name}')
            else:
                guys_list.append('😎 Человек без имени и телеги')
        guys = '\n'.join(guys_list)
        return start, guys

    def make_wish(self, whom):
        n = len(whom)
        start = str()
        guys = str()

        # create wish with Balaboba
        congratulation = random.choice(self.wishes)
        wish_words = congratulation.split(' ')
        if len(wish_words) > 9:
            prompt = ' '.join(wish_words[:8])  # you can tune length of prompt
        else:
            prompt = ' '.join(wish_words[:4])
        wish = self.bb.balaboba(prompt, intro=self.intro.number)
        while not wish:  # waiting for the balaboba to finish its work
            time.sleep(1)
        end = random.choice(['\n\nНакидайте стикеросов!',
                             '\n\nВыпускайте собак!',
                             '\n\nКидайте собак!'])

        if n == 1:
            start, guys = self.parse_one(whom)
        elif n > 1:
            start, guys = self.parse_many(whom)
        if len(guys) > 0:
            wish = start + guys + '\n\n' + wish + end
            return wish
