from bearlibterminal import terminal as blt


class MessageLog:
    def __init__(self):
        self.total_height = 7
        self.texts = []
        self.heights = []

    def update_heights(self, width):
        self.heights = [blt.measure(text, width)[1] for text in self.texts]
        # print(self.heights)
        # recompute total height, including the blank lines between messages
        if len(self.texts) <= self.total_height:
            return
        self.total_height = len(self.texts)  # + sum(self.heights) + len(self.texts) - 1

    def append(self, message):
        self.texts.append(message)

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, key):
        return self.texts[key], self.heights[key]
