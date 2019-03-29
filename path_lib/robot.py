class Robot:
    def __init__(self, x=0, y=0, *args, **kwargs):
        self.x, self.y = x, y
        self.y_vel = self.x_vel = 0

        self.config(x, y, *args, **kwargs)

    def config(x, y, *args, **kwargs): pass

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def get_x(self): return round(self.x, 5)
    def get_y(self): return round(self.y, 5)
    def get_x_vel(self): return round(self.x_vel, 5)
    def get_y_vel(self): return round(self.y_vel, 5)

    def set_x_vel(self, x_vel):
        self.x_vel = x_vel

    def set_y_vel(self, y_vel):
        self.y_vel = y_vel

    def brake(self):
        self.set_x_vel(0)
        self.set_y_vel(0)

    def update(self):
        self.move()

    def __str__(self): return "<{} pos: ({}, {}) vel: ({}, {})>".format(
        type(self).__name__,
        self.get_x(),
        self.get_y(),
        self.get_x_vel(),
        self.get_y_vel()
        )