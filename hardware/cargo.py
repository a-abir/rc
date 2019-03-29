from wpilib import *

from .switch import RevLimitSwitch as LimitSwitch
from .talon import Talon, Victor
from .constants import CargoGrabberStates
from .timer import Timer


class CargoGrabber:
    # ROTATE_UP_SPEED = 0.25
    # ROTATE_DOWN_FAST_SPEED = -0.25
    # ROTATE_DOWN_HOLD_SPEED = -0.04
    # INTAKE_SPEED = -0.5
    # ROTATE_UP_SPEED = -0.25
    # ROTATE_DOWN_FAST_SPEED = 0.25
    # ROTATE_DOWN_HOLD_SPEED = 0.04
    # INTAKE_SPEED = -0.5
    ROTATE_UP_SPEED = 0.25
    ROTATE_DOWN_FAST_SPEED = -0.25
    ROTATE_DOWN_HOLD_SPEED = -0.1
    INTAKE_SPEED = -0.5
    LIMIT_SWITCH_CHANNEL = 3

    def __init__(self, rotate_mechanism_motor_id, intake_cargo_motor_id):
        self.rotate_mechanism_motor = Talon(rotate_mechanism_motor_id)
        self.intake_cargo_motor = Victor(intake_cargo_motor_id)
        # self.rotate_mechanism_motor = Victor(rotate_mechanism_motor_id)
        # self.intake_cargo_motor = Talon(intake_cargo_motor_id)

        self.limit_switch = LimitSwitch(self.LIMIT_SWITCH_CHANNEL)

        self.timer = Timer()
        self.stop()

    def update(self):
        if self.is_stopping():
            self.brake_intake()
            self.brake_rotate()

        elif self.is_lowering():
            self.intake()
            self.rotate_down()
            
            self.timer.wait(1)

            if self.timer.is_done():
                self.hold()

        elif self.is_holding():
            self.intake()
            self.hold_intake_down()


        elif self.is_raising():
            self.rotate_up()
            self.intake()
            
            self.timer.wait(1)

            if self.timer.is_done():
                self.stop()

    def hold_intake_up(self): self.set_rotate_motor(self.ROTATE_UP_SPEED/2)
    def rotate_up(self): self.set_rotate_motor(self.ROTATE_UP_SPEED)
    def rotate_down(self): self.set_rotate_motor(self.ROTATE_DOWN_FAST_SPEED)
    def hold_intake_down(self): self.set_rotate_motor(self.ROTATE_DOWN_HOLD_SPEED)

    def get_cargo(self):
        self.lower()

    def stop_getting_cargo(self):
        self.raise_()


    def lower(self): self.state = CargoGrabberStates.Lowering
    def raise_(self): self.state = CargoGrabberStates.Raising
    def hold(self): self.state = CargoGrabberStates.Holding
    def stop(self): self.state = CargoGrabberStates.Stopping

    def is_lowering(self): return self.state == CargoGrabberStates.Lowering
    def is_raising(self): return self.state == CargoGrabberStates.Raising
    def is_holding(self): return self.state == CargoGrabberStates.Holding
    def is_stopping(self): return self.state == CargoGrabberStates.Stopping

    def set_state(self, state):
        self.state = state

    def intake(self): self.set_intake_motor(self.INTAKE_SPEED)

    def brake_rotate(self): self.set_rotate_motor(0)

    def brake_intake(self): self.set_intake_motor(0)

    def set_rotate_motor(self, value):
        '''
        Private method, do not use!
        '''
        self.rotate_mechanism_motor.set(value)

    def set_intake_motor(self, value):
        '''
        Private method, do not use!
        '''
        self.intake_cargo_motor.set(value)
