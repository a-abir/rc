from wpilib import DigitalInput


class RevLimitSwitch(DigitalInput):
    def is_triggered(self): return not self.get()