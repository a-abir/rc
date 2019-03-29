from math import pi
from .talon import Talon


class Encoder:
    WHEEL_DIAMETER = 4 / 12
    ENCODER_COUNTS_PER_REV = 4096
    PIDIDX = 0

    def __init__(self, talon):
        self.talon = talon
    
    def setInverted(self, inverted):
        '''
        Inverts the encoder
        '''
        self.talon.setSensorPhase(inverted)

    def reset(self):
        self.talon.setSelectedSensorPosition(0, self.PIDIDX, 0)
        # self.talon.setQuadraturePosition(0, 0)
    
    def get(self):
        return int(self.talon.getSelectedSensorPosition(self.PIDIDX) / -4.633)
        # return abs(self.talon.getQuadraturePosition())

    def get_distance(self, diameter):
        encoder_constant = (
            (1 / self.ENCODER_COUNTS_PER_REV) * diameter * pi
        )
        return self.get() * encoder_constant