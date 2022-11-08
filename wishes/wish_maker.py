class WishMaker:

    def __init__(self):
        pass

    def make_wish(self, whom):
        n = len(whom)
        wish = None

        if n == 1:
            name = whom[0]
            tg_username = whom[1]
            wish = f'Сегодня днюху празднует {name} ({tg_username})!\n\nНакидайте стикеросов!'
        elif n > 1:
            start_phrase = 'Сегодня празднуют ДР:\n'
            guys = list()
            for i in range(len(whom)):
                guy = f'{whom[i][0]}  ({whom[i][1]})'
                guys.append(guy)
            body = '\n'.join(guys)
            end_phrase = '\n\nНакидайте стикеросов!'
            wish = start_phrase + body + end_phrase

        return wish
