from wpilib.drive import DifferentialDrive

from .gyro import Gyro
from .encoder import Encoder
from .talon import Talon, Victor
from .timer import Timer
from .solenoid import Solenoid
from .constants import ShifterStates


class GearShifter(Solenoid):
    def __init__(self, low_gear_port, high_gear_port):
        super().__init__(
            low_gear_port,
            high_gear_port
        )
        self.set_low_gear()
        self.timer = Timer()
        self.timer.wait(1)
        
    # Setters
    def set_low_gear(self):
        self.set_forward()
        self.set_gearing_state(ShifterStates.LowGear)

    def set_high_gear(self):
        self.set_reverse()
        self.set_gearing_state(ShifterStates.HighGear)

    def set_gearing_state(self, state):
        self.gearing_state = state

    def shift(self):
        self.timer.wait(1)
        if self.timer.is_done():
            if self.is_in_low_gear():
                self.set_high_gear()
            else:
                self.set_low_gear()

    # Getters
    def get_gearing_state(self): return self.gearing_state

    def is_in_low_gear(self):
        return self.get_gearing_state() == ShifterStates.LowGear

    def is_in_high_gear(self):
        return not self.is_in_low_gear()


class Chassis:
    def __init__(self, left_master_id, right_master_id, low_gear_solenoid_port=0, high_gear_solenoid_port=1, left_slave_ids=[], right_slave_ids=[]):
        # Create a GearShifter with the specified low gear port on the PCM
        # and the high gear port on the PCM.
        self.shifter_actuator = GearShifter(
            low_gear_solenoid_port,
            high_gear_solenoid_port
        )

        # Create the motor controllers that will read the encoders and control
        # the other motors on the drive train.
        # these are the only talons.
        self.left_master = Talon(left_master_id)
        self.right_master = Talon(right_master_id)

        # These set whether or not the encoders on the left and right masters are inverted
        self.left_master.setSensorPhase(False)
        self.right_master.setSensorPhase(False)

        # These are the slave motors for the drive train.
        # MAKE SURE THAT THESE ARE THE RIGHT TYPE OF MOTOR CONTROLLER
        for left_slave_id in left_slave_ids:
            # Use talon as a placeholder for now, might be victor later
            Victor(left_slave_id).follow(self.left_master)
        for right_slave_id in right_slave_ids:
            # Use talon as a placeholder for now, might be victor later
            Victor(right_slave_id).follow(self.right_master)

        # Create encoders for left and right motors
        self.left_encoder = Encoder(self.left_master)
        self.right_encoder = Encoder(self.right_master)
        # For some reason, right encoder is inverted
        self.right_encoder.setInverted(True)

        # Create gyro for adjusting robot heading during path
        self.gyro = Gyro()

        # Create a wpilib drivetrain that the chassis will wrap around
        self.drive = DifferentialDrive(self.left_master, self.right_master)

        self.reset_sensors()

        # self.path = 

    def shift(self): self.shifter_actuator.shift()

    def reset_sensors(self):
        self.left_encoder.reset()
        self.right_encoder.reset()
        self.gyro.reset()

    def update(self): pass
        # print("angle", self.gyro.getAngle())

    def get_raw_left_distance(self):
        return self.left_encoder.get()

    def get_raw_right_distance(self):
        return self.right_encoder.get()

    def arcade_drive(self, forward, rotation):
        '''
        Drives the robot using arcade drive
        '''
        self.drive.arcadeDrive(forward, rotation)

    def tank_drive(self, left, right):
        '''
        Drives the robot using tank drive
        '''
        self.drive.tankDrive(left, right)

    def drive_back(self, speed):
        '''
        Drives the robot backward at speed `speed`
        '''
        self.arcade_drive(-speed, 0)

    def drive_forward(self, speed):
        '''
        Drives the robot forward at speed `speed`
        '''
        self.arcade_drive(speed, 0)

    def set_low_gear(self):  self.shifter_actuator.set_low_gear()

    def set_high_gear(self): self.shifter_actuator.set_high_gear()

    def is_in_low_gear(self): return self.shifter_actuator.is_in_low_gear()

    def is_in_high_gear(self): return not self.is_in_low_gear()