import scripts.tools as tools


class ConvertTile:
    def __init__(self):
        # для удобства храним все спрайты в общем словаре: который импортируем
        self.tile_images = {
            '1': [tools.load_image('platform/platform.png'), '1'],
            '2': [tools.load_image('platform/platform_horizontal.png'), '2'],
            '3': [tools.load_image('platform/platform_vertical.png'), '3'],
            '4-': [tools.load_image('platform/platform.png'), '4'],
            '5-': [tools.load_image('platform/platform_horizontal.png'), '5'],
            '6-': [tools.load_image('platform/platform_vertical.png'), '6'],
            '7': [tools.load_image('disappearing_block/disappearing_block_1.png', -2), '7'],
            '8': [tools.load_image('disappearing_block/disappearing_block_2.png', -2), '8'],
            '9': [tools.load_image('disappearing_block/disappearing_block_3.png', -2), '9'],
            '10': [tools.load_image('spike/spike_classic.png'), 's'],
            '11': [tools.load_image('dirt/dirt.png'), 'd'],
            '12-': [tools.load_image('dirt/dirt.png'), 'D'],
            '13': [tools.load_image('dirt/dirt_up.png'), 'u'],
            '14-': [tools.load_image('dirt/dirt_up.png'), 'U'],
            '15': [tools.load_image('dirt/dirt_down.png'), 'h'],
            '16-': [tools.load_image('dirt/dirt_down.png'), 'H'],
            '17': [tools.load_image('dirt/dirt_left.png'), 'l'],
            '18-': [tools.load_image('dirt/dirt_left.png'), 'L'],
            '19': [tools.load_image('dirt/dirt_right.png'), 'r'],
            '20-': [tools.load_image('dirt/dirt_right.png'), 'R'],
            '21': [tools.load_image('dirt/dirt_up_left.png'), 'q'],
            '22-': [tools.load_image('dirt/dirt_up_left.png'), 'Q'],
            '23': [tools.load_image('dirt/dirt_down_left.png'), 'w'],
            '24-': [tools.load_image('dirt/dirt_down_left.png'), 'W'],
            '25': [tools.load_image('dirt/dirt_up_right.png'), 'e'],
            '26-': [tools.load_image('dirt/dirt_up_right.png'), 'E'],
            '27': [tools.load_image('dirt/dirt_down_right.png'), 't'],
            '28-': [tools.load_image('dirt/dirt_down_right.png'), 'T'],
            '29': [tools.load_image('player/Knight.png'), '@'],
            '30': [tools.load_image('goblin/goblin_attack/attack1.png'), 'g']
        }

    def return_symbol(self, index) -> str:
        """
        Метод конвертирования индекса в символ блока
        :param index: int
        :return: str
        """
        count = 0
        for key, value in self.tile_images.items():
            if index == count:
                return value[1]
            count += 1

    def return_index(self, symbol) -> int:
        """
        Метод конвертирования символа в индекс блока
        :param symbol: str
        :return: int
        """
        count = 0
        for key, value in self.tile_images.items():
            if symbol == value[1]:
                return count
            count += 1
