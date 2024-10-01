class spell_number:
    def __init__(self, num):
        self.num = num

    def spell(self):
        return self.num

    def __str__(self):
        return str(self.spell())
