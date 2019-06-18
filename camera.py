class Camera:
    def __init__(self, width, height, x=0, y=0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def move_camera(self, target_x, target_y, game_map):
        # Новые координаты камеры, чтобы цель была по центру экрана
        x = int(target_x - self.width / 2)
        y = int(target_y - self.height / 2)

        (self.x, self.y) = (x, y)
        # print("camera coords", self.x, self.y)

    def to_camera_coordinates(self, x, y):
        # Конвертируем координаты на карте в координаты на экране
        (x, y) = (x - self.x, y - self.y)
        # if (x < 0 or y < 0 or x >= self.width or y >= self.height):
        #    return(None, None)
        return x, y

    def to_map_coordinates(self, x, y):
        # Конвертируем координаты на экране в координаты на карте
        (x, y) = (x + self.x, y + self.y)
        # print("Camera_x ", self.x)
        # print("Camera_y ", self.y)
        # print("map_cor", map_x, map_y)
        return x, y
