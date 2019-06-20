from bearlibterminal import terminal as blt
from math import ceil


class FrameWithScrollbar:
    def __init__(self, contents, color):
        self.offset = 0
        self.width = 0
        self.height = 0
        self.scrollbar_height = 0
        self.scrollbar_column = 0
        self.scrollbar_offset = 0
        self.left = self.top = self.width = self.height = 0
        self.contents = contents
        self.color = color

    def update_geometry(self, left, top, width, height):
        # Save current scroll position
        current_offset_percentage = self.offset / self.contents.total_height

        # Update frame dimensions
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        # Calculate new message list height
        self.contents.update_heights(width)

        # Scrollbar
        self.scrollbar_height = min(
            int(ceil(self.height * self.height / self.contents.total_height)),
            self.height)

        # Try to recover scroll position
        self.offset = int(self.contents.total_height * current_offset_percentage)
        self.offset = min(self.offset, self.contents.total_height - self.height)
        if self.contents.total_height <= self.height:
            self.offset = 0

    def scroll(self, dy):
        print('Must scroll', dy)
        self.offset = max(0, min(self.contents.total_height - self.height, self.offset + dy))
        print('self.offset', self.offset)

    def draw(self):
        x = self.top
        frame_height = self.height
        scrollbar_height = self.scrollbar_height
        frame_offset = self.offset
        messages_len = self.contents.total_height
        cell_height = blt.state(blt.TK_CELL_HEIGHT)
        blt.color(self.color)
        self.scrollbar_column = self.left + self.width
        self.scrollbar_offset = int(
            (x + (frame_height - scrollbar_height) * (1 - frame_offset / (messages_len - frame_height + 1)))
            * cell_height)
        # top line
        for i in range(self.left - 1, self.left + self.width + 2):
            blt.put(i, self.top - 1, '+')
        # bottom line
        for i in range(self.left - 1, self.left + self.width + 2):
            blt.put(i, self.top + self.height, '+')
        # left line
        for i in range(self.top - 1, self.top + self.height + 1):
            blt.put(self.left - 1, i, '+')
        # right line
        for i in range(self.top - 1, self.top + self.height + 1):
            blt.put(self.left + self.width + 1, i, '+')
        # scrollbar
        for i in range(self.scrollbar_height):
            blt.put_ext(self.scrollbar_column, i, 0, self.scrollbar_offset, 0x2588)
