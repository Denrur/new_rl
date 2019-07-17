import textwrap

from bearlibterminal import terminal as blt


class MessageLog:
    def __init__(self):
        self.width = 0
        self.total_height = 7
        self.texts = []
        self.heights = []

    def update_heights(self, width):
        self.width = width
        self.heights = [blt.measure(text, width)[1] for text in self.texts]
        # print('log height', self.heights)
        # recompute total height, including the blank lines between messages
        if len(self.texts) <= self.total_height:
            return
        self.total_height = len(self.texts) + sum(self.heights) - 1

    def append(self, message):
        new_msg_lines = textwrap.wrap(message, self.width)

        for line in new_msg_lines:
            self.texts.append(line)

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, key):
        return self.texts[key], self.heights[key]
