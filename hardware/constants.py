from enum import Enum


class IntakeStates(Enum):
    '''
    The states that the intake can be in
    '''

    Idle = 0
    Intaking = 1
    SlowIntaking = 2
    Shooting = 3


class ElevatorStates(Enum):
    '''
    The states that the elevator can be in
    '''

    GoingUp = 0
    GoingDown = 1


class ShifterStates(Enum):
    '''
    The states that the gear shifter can be in
    '''

    LowGear = 0
    HighGear = 1


class HatchHolderStates(Enum):
    Grabbing = 0
    Holding = 1
    Dropping = 2
    Stopping = 3
    Intaking = 4


class CargoGrabberStates(Enum):
    Lowering = 0
    Holding = 1
    Raising = 2
    Stopping = 3
