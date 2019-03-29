# from wpilib import *

from .solenoid import Solenoid
from .talon import Talon
from .timer import Timer

from .constants import HatchHolderStates


class HatchFloorGrabber:
    ROTATE_SPEED = -0.2
    INTAKE_SPEED = -1

    def __init__(self, rotate_mechanism_motor_id, intake_hatch_motor_id):
        self.rotate_mechanism_motor = Talon(rotate_mechanism_motor_id)
        self.intake_hatch_motor = Talon(intake_hatch_motor_id)

    def update(self): pass

    def hold_up(self): self.set_rotate_motor(self.ROTATE_SPEED/2)

    def rotate_up(self): self.set_rotate_motor(self.ROTATE_SPEED)

    def rotate_down(self): self.set_rotate_motor(-self.ROTATE_SPEED)

    def brake_rotate(self): self.set_rotate_motor(0)

    def intake(self): self.set_intake_motor(self.INTAKE_SPEED)
    def outtake(self): self.set_intake_motor(-self.INTAKE_SPEED)
    
    def brake_intake(self): self.set_intake_motor(0)

    def set_rotate_motor(self, value):
        self.rotate_mechanism_motor.set(value)

    def set_intake_motor(self, value):
        self.intake_hatch_motor.set(value)


class HatchHolder:
    def __init__(self, extend_port, retract_port, open_port, close_port):
        self.extend_actuator = Solenoid(extend_port, retract_port)
        self.holder_actuator = Solenoid(open_port, close_port)

        self.timer = Timer()
        self.state = HatchHolderStates.Stopping
        self.retract()
        self.open()
        self.hold()

    def update(self):
        if self.is_grabbing():
            # print("grabbing")
            self.extend()
            self.close()
            self.timer.wait(1)

            if self.timer.is_done():
                print("timer done")
                self.open()
                self.hold()

        elif self.is_holding():
            # print("holding")
            self.timer.wait(0.5)

            self.open()
            if self.timer.is_done():
                self.retract()

        elif self.is_dropping():
            # print("dropping")
            self.extend()
            self.open()
            self.timer.wait(0.5)

            if self.timer.is_done():
                self.close()
                self.stop()

        elif self.is_stopping():
            # print("stopping")
            self.timer.wait(0.5)

            self.close()
            if self.timer.is_done():
                self.retract()

        elif self.is_intaking():
            self.close()
            self.retract()
            # print("stopping")
            # self.timer.wait(0.5)

            # self.close()
            # if self.timer.is_done():
            #     self.retract()


    def grab(self):
        self.set_state(HatchHolderStates.Grabbing)

    def hold(self):
        self.set_state(HatchHolderStates.Holding)

    def drop(self):
        self.set_state(HatchHolderStates.Dropping)

    def stop(self):
        self.set_state(HatchHolderStates.Stopping)

    def intake(self):
        self.set_state(HatchHolderStates.Intaking)

    def is_dropping(self):
        return self.get_state() == HatchHolderStates.Dropping

    def is_grabbing(self):
        return self.get_state() == HatchHolderStates.Grabbing

    def is_holding(self):
        return self.get_state() == HatchHolderStates.Holding

    def is_stopping(self):
        return self.get_state() == HatchHolderStates.Stopping

    def is_intaking(self):
        return self.get_state() == HatchHolderStates.Intaking

    def get_state(self): return self.state

    def set_state(self, state): self.state = state

    def extend(self):
        '''
        This is a private method, do not use!

        This extends the holder forward
        '''
        self.extend_actuator.extend()

    def retract(self):
        '''
        This is a private method, do not use!

        This retracts the holder inward
        '''
        self.extend_actuator.retract()

    def open(self):
        '''
        This is a private method, do not use!

        This opens the holder
        '''
        self.holder_actuator.extend()

    def close(self):
        '''
        This is a private method, do not use!

        This closes the holder
        '''
        self.holder_actuator.retract()
