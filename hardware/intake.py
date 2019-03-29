from math import pi
from wpilib import *
from ctre import PigeonIMU as Pigeon
from networktables.util import ntproperty

from .talon import Talon
from .constants import IntakeStates


class Intake:
    '''
    Object that controls the Elevator on the robot
    '''
    def __init__(self, front_motor_id, back_motor_id):
        '''
        Insantiate Intake object on our bot.

        It takes the ids of the: left front motor, right front motor, left back motor, right back motor.
        In that order.
        '''
        self.State = IntakeStates.Idle
        self.front_motor = Talon(front_motor_id)
        self.back_motor  = Talon(back_motor_id)

    def update(self):
        '''
        This updates our Intake object.
        Run this in your periodic methods of your robot.
        '''
        if self.is_idle():
            self.set_motors_brake()
        elif self.is_intaking():
            self.set_motors_intake()
        elif self.is_slow_intaking():
            self.set_motors_slow_intake()
        elif self.is_shooting():
            self.set_motors_shoot()

    def idle(self): self.set_state(IntakeStates.Idle)
    def shoot(self): self.set_state(IntakeStates.Shooting)
    def intake(self): self.set_state(IntakeStates.Intaking)
    def slow_intake(self): self.set_state(IntakeStates.SlowIntaking)

    def is_idle(self): return self.State == IntakeStates.Idle
    def is_intaking(self): return self.State == IntakeStates.Intaking
    def is_slow_intaking(self): return self.State == IntakeStates.SlowIntaking
    def is_shooting(self): return self.State == IntakeStates.Shooting

    def set_motors_brake(self):
        '''
        Stop all motor movement in the intake.
        
        This is a private method, do not use me!
        '''
        self.set_front_back(0, 0)

    def set_motors_intake(self):
        '''
        Set the front and back motor speeds for intaking the ball.

        This is a private method, do not use me!
        '''
        # Assuming we intake from the front
        # Rotate the front wheels to intake towards the back of the bot
        self.set_front_back(back_speed=-1)

    def set_motors_slow_intake(self):
        '''
        Set the front and back motor speeds for intaking the ball.

        This is a private method, do not use me!
        '''
        # Assuming we intake from the front
        # Rotate the front wheels to intake towards the back of the bot
        self.set_front_back(front_speed=-0.5, back_speed=-0.9)

    def set_motors_shoot(self):
        '''
        Set the front and back motor speeds for intaking the ball.
        
        This is a private method, do not use me!
        '''
        # Assuming we shoot towards the front
        # Rotate the all wheels to outake towards the front of the bot
        self.set_front_back(front_speed=1, back_speed=-1)

    def set_front_back(self, front_speed=0, back_speed=0):
        '''
        Sets the speeds for the front motors and back motors.

        Mind you, this automatically inverts the left and right motors for you.
        It runs the front left motor opposite the front right motor.

        Fix this so that negative means intaking towards the back of the bot.
        
        This is a private method, do not use me!
        '''
        # we have to flip directions on jake
        self.front_motor.set(front_speed)
        self.back_motor.set(back_speed)
        # self.front_motor.set(front_speed)
        # self.back_motor.set(back_speed)

    def set_state(self, state): self.State = state
