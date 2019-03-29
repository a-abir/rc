from wpilib import Compressor, DoubleSolenoid


Forward = DoubleSolenoid.Value.kForward
Reverse = DoubleSolenoid.Value.kReverse


class Solenoid:
    compressor = Compressor()
    PCM_ID = 20

    def __init__(self, forward_port, reverse_port):
        '''
        Creates a Solenoid object.

        Takes two arguments, forward_port, and reverse_port.
        These are the port numbers on the PCM that each solenoid
        in the doublesolenoid is wired to.

        The doublesolenoid is the solenoid that can invert pushing and pulling
        on an actuator.
        '''

        self.wpilib_solenoid = DoubleSolenoid(
            self.PCM_ID,
            forward_port,
            reverse_port
        )

        self.forward_port = forward_port
        self.reverse_port = reverse_port

        self.inverted = False

        self.set_forward()

    def set_forward(self):
        self.set_wrapped_solenoid(Reverse if self.is_inverted() else Forward)

    def set_reverse(self):
        self.set_wrapped_solenoid(Forward if self.is_inverted() else Reverse)

    def extend(self): self.set_forward()

    def retract(self): self.set_reverse()

    def set_invert(self, invert):
        '''
        If `invert` is true, this inverts the Solenoids
        where forwards is reverse and vice versa.

        If `invert` is false, it brings it back to its normal state.
        '''
        self.inverted = invert

    def is_inverted(self): return self.inverted

    def set_wrapped_solenoid(self, value):
        self.wpilib_solenoid.set(value)
