from math import pi
from wpilib import *
from ctre import PigeonIMU as Pigeon
from networktables.util import ntproperty

from .talon import Talon
from .constants import ElevatorStates


class Elevator:
    '''
    Object that controls the Elevator on the robot
    '''
    PIDIDX = 0

    # This controls the angle at which the elevator
    # decides the robot is tipping.
    TippingBound = 11

    PigeonCanID = 19
    OUTPUT_SHAFT_DIAMETER = 1.76 / 12  # in feet
    PID_SPEED = 0.6

    UP_SPEED = 0.30
    DOWN_SPEED = -0.18
    # UP_SPEED = 0.2
    # DOWN_SPEED = -0.05
    SLOW_DOWN_SPEED = -0.02
    HOLD_SPEED = 0.1

    KP = ntproperty("/SmartDashboard/KP", 0, writeDefault=True)
    KI = 0
    KD = ntproperty("/SmartDashboard/KD", 0, writeDefault=True)

    def __init__(self, master_id, slave_ids):
        '''
        Insantiate Elevator object on our bot.

        It takes the ids of the motors controlling the elevator as
        a variable list of arguments.

        Instantiate it like this: `Elevator(1, 2, 3, 4)`, assuming
        motors with ids 1, 2, 3, and 4 are
        driving your elevator.
        '''
        # The pigeon is a small gyro/accelerometer with 9 degrees
        # of freedom on the bot.

        # When it boots up, we want it to zero itself. 
        # However, there is no reset or calibrate
        # function on the pigeon. Instead, we take the initial values 
        # that the gyro reads, and offset
        # the gyro values from then on by those initial values.

        # Effectively, we zero the pigeon.
        self.commanded_position = 0
        self.PitchOffset = 0
        self.RollOffset = 0
        
        try:
            self.pigeon = Pigeon(self.PigeonCanID)
        except:
            print("===| ERROR |===> Couldn't find pigeon")

        self.PitchOffset = self.get_pitch()
        self.RollOffset = self.get_roll()

        # Here we create an instance of the Talon with the master id.
        # All of the other motor ids given will folow the master motor.
        self.master_talon = Talon(master_id)
        self.talons = [self.master_talon]
        for motor_id in slave_ids:
            m = Talon(motor_id)
            m.follow(self.master_talon)
            m.setInverted(True)
            self.talons.append(m)

        # Then we select the feedback sensor on the master talon.
        # We're using a CTRE Mag encoder plugged into the master talon,
        # so we'll set it to follow a QuadEncoder.
        self.master_talon.configSelectedFeedbackSensor(
            self.master_talon.FeedbackDevice.QuadEncoder, self.PIDIDX, 10
        )
        self.master_talon.setSelectedSensorPosition(0, self.PIDIDX, 10)

        # Next, we make sure the talon and the sensor aren't inverted.
        # This can be configured as needed.
        self.master_talon.setInverted(True)
        self.master_talon.setSensorPhase(True)

        # Then we enable voltage compensation on the master 
        # talon to keep the motor outputs
        # consistent regardless of our battery's charge.
        self.master_talon.enableVoltageCompensation(True)
        self.master_talon.configVoltageCompSaturation(12, 0)
        self.master_talon.configClosedLoopPeakOutput(1, self.PID_SPEED, 0)
        # Set PID for elevator
        self.set_state(True)
        # Lastly, we configure the PID values for going up/down the elevator
        self.set_p_up(0.065)
        self.set_i_up(0)
        self.set_d_up(1.000)

        # self.set_p_down(0)
        # self.set_i_down(0)
        # self.set_d_down(0)

        Elevator.low(self)
    
    def reset_sensors(self):
        self.master_talon.zero_encoder()

    def stop(self):
        self.master_talon.set(self.HOLD_SPEED)

    def up(self):
        self.master_talon.set(self.UP_SPEED)
    
    def down(self):
        self.master_talon.set(self.DOWN_SPEED)
    
    def slow_down(self):
        self.master_talon.set(self.SLOW_DOWN_SPEED)
    
    def zero(self):
        self.set_commanded_position(0)
    
    def low(self):
        self.set_commanded_position(9/12 * 3.14)
    
    def mid(self):
        self.set_commanded_position(35.5/12 * 3.14)

    def high(self):
        self.set_commanded_position(59.5/12 * 3.14)

    def cargo_ship(self):
        self.set_commanded_position(1.8687 * 3.14)

    def update(self):
        '''
        This updates our Elevator object.
        Run this in your periodic methods of your robot.
        '''

        # set the state based on whether or not the elevator
        # is going up
        self.set_state(True)
        # self.set_p_up(self.KP)
        # self.set_d_up(self.KD)
        if self.get_actual_position() < 0:
            self.reset_sensors()


        if self.is_going_up() and self.get_commanded_position() != 0:
            print(
                "error", round(self.master_talon.getClosedLoopError(), 2),
                "target", round(self.master_talon.getClosedLoopTarget(), 2)
                )

            self.go_to_feet(
                self.get_commanded_position()
                )
        elif self.get_commanded_position() == 0:
            self.slow_down()
        else:
            self.down()

    def set_commanded_position(self, position):
        '''
        Sets the commanded position of the elevator.
        Use this to control the elevator
        '''
        self.commanded_position = position

    def go_to_feet(self, commanded_position):
        '''
        Private method, do not use!!

        Commands the elevator to go to a specific position in feet.
        '''
        commanded_position_in_talon_units = commanded_position / self.OUTPUT_SHAFT_DIAMETER / pi * 4096
        self.master_talon.set(
            Talon.ControlMode.Position,
            commanded_position_in_talon_units
        )

    def is_tipping_backward(self):
        '''
        Detects whether or not the robot is tipping forward
        '''
        return self.get_pitch() < -self.TippingBound

    def is_tipping_forward(self):
        '''
        Detects whether or not the robot is tipping back
        '''
        return self.get_pitch() > self.TippingBound

    def is_tipping(self):
        '''
        Detects whether or not the robot is tipping over
        '''
        # return abs(self.get_pitch()) > self.TippingBound or abs(self.get_roll()) > self.TippingBound
        return False

    def get_gyro_data(self):
        try:
            return self.pigeon.getAccumGyro()
        except NotImplementedError:
            return [0, 0, 0]

    def get_pitch(self):
        return round(
            round(self.get_gyro_data()[1], 2) - self.PitchOffset, 2
            )

    def get_roll(self):
        return round(round(self.get_gyro_data()[2], 2) - self.RollOffset, 2)

    def set_f_up(self, f): self.set_f(f, slot=1)

    def set_p_up(self, p): self.set_p(p, slot=1)

    def set_i_up(self, i): self.set_i(i, slot=1)

    def set_d_up(self, d): self.set_d(d, slot=1)

    def set_f_down(self, f): self.set_f(f, slot=0)

    def set_p_down(self, p): self.set_p(p, slot=0)

    def set_i_down(self, i): self.set_i(i, slot=0)

    def set_d_down(self, d): self.set_d(d, slot=0)

    def is_going_up(self):
        '''
        Detects whether or not the elevator is moving up or down
        '''
        if abs(self.get_commanded_position()) > abs(self.get_actual_position()):
            return True
        return False

    def get_commanded_position(self):
        '''
        Gets the position of the elevator commanded by the user
        '''
        return self.commanded_position

    def get_actual_position(self):
        '''
        Gets the position of the elevator in reality
        '''
        return self.master_talon.get_feet(self.OUTPUT_SHAFT_DIAMETER)

    def set_state(self, is_going_up):
        '''
        Selects the PID profile for the commanded direction of the elevator

        Private method, do not use!
        '''
        self.master_talon.selectProfileSlot(int(is_going_up), self.PIDIDX)

    def set_f(self, f, slot=0):
        '''
        Sets the F gain for the PID at the specified slot

        Private method, do not use!
        '''
        self.master_talon.config_kF(slot, f, 0)

    def set_p(self, p, slot=0):
        '''
        Sets the P gain for the PID at the specified slot
        
        Private method, do not use!
        '''
        self.master_talon.config_kP(slot, p, 0)

    def set_i(self, i, slot=0):
        '''
        Sets the I gain for the PID at the specified slot
        
        Private method, do not use!
        '''
        self.master_talon.config_kI(slot, i, 0)

    def set_d(self, d, slot=0):
        '''
        Sets the D gain for the PID at the specified slot
        
        Private method, do not use!
        '''
        self.master_talon.config_kD(slot, d, 0)
