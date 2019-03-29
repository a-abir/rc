from math import pi
from ctre import WPI_TalonSRX, WPI_VictorSPX


class Talon(WPI_TalonSRX):
    def zero_encoder(self): self.setQuadraturePosition(0, 0)

    def get_inches(self, output_diameter_in_inches):
        return output_diameter_in_inches * (self.getQuadraturePosition() / 4096) * pi

    def get_feet(self, output_diameter_in_feet):
        return self.get_inches(output_diameter_in_feet * 12) / 12


class Victor(WPI_VictorSPX):
    pass
