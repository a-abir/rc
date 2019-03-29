from .path import Segment
import pathfinder as pf
from remote_path import RemotePath
from pathfinder.followers import EncoderFollower
from math import degrees


class Trajectory(Segment):
    '''
    This class handles all of the pathfinding for you.
    Call this with the instance of your robot class.

    The goal is to have more than one of these in use at a time.
    
    We generate the remote path when we start this segment of the path.

    You must run the server to use this!
    '''

    # Pathfinder constants (r^2 is 0.9867)
    WHEEL_BASE = 2.35              # feet
    WHEEL_DIAMETER = 4/12         # feet
    ENCODER_COUNTS_PER_REV = 4096 # counts per revolution of wheel
    # KP = 0.431
    # KP = 1
    # KP = 0.3
    KP = 0.6
    # KP = 0
    KD = 0.04
    
    KV = 0.1409 # V / (m * s)
    KA = 0.1084 # V / (m * s^2)
    V_INTERCEPT = 2.2708 # V

    def __init__(self, waypoints):
        super().__init__()
        '''
        @param waypoints - The waypoints for the remote path
        '''
        # This is the cause of the potential undefined behavior
        self.remote_path = RemotePath()
        self.waypoints = waypoints

        # These are the encoder followers used by pathfinder
        self.left_encoder_follower = None
        self.right_encoder_follower = None
        # self.start_angle = 0

    def config(self, robot):
        '''
        Init for following the trajectory!
        '''

        # # Reset robot 
        # robot.chassis.reset_sensors()

        # self.start_angle = robot.chassis.gyro.getAngle()


        # Generate remote trajectory
        trajectory = self.remote_path.generate_remote_path(self.waypoints)
        while not trajectory:
            trajectory = self.remote_path.generate_remote_path(self.waypoints)

        print("Trajectory", trajectory)
        trajectory = trajectory.modify(self.WHEEL_BASE)

        self.left_encoder_follower = EncoderFollower(trajectory.getLeftTrajectory())
        self.right_encoder_follower = EncoderFollower(trajectory.getRightTrajectory())

        # Configure PIDVA for left encoder follower
        self.left_encoder_follower.configurePIDVA(self.KP, 0, self.KD, self.KV, self.KA)

        # Give left encoder follower encoder data and wheel size
        self.left_encoder_follower.configureEncoder(
            robot.chassis.get_raw_left_distance(),
            self.ENCODER_COUNTS_PER_REV,
            self.WHEEL_DIAMETER
        )

        # Configure PIDVA for right encoder follower
        self.right_encoder_follower.configurePIDVA(self.KP, 0, self.KD, self.KV, self.KA)

        # Give right encoder follower encoder data and wheel size
        self.right_encoder_follower.configureEncoder(
            robot.chassis.get_raw_right_distance(),
            self.ENCODER_COUNTS_PER_REV,
            self.WHEEL_DIAMETER
        )

        # robot.chassis.reset_sensors()

    def update(self, robot):
        short = lambda n: round(n, 2)


        l = self.left_encoder_follower.calculate(
            robot.chassis.get_raw_left_distance()
        )

        r = self.right_encoder_follower.calculate(
            robot.chassis.get_raw_right_distance()
        )

        gyro_heading = robot.chassis.gyro.getAngle()
        desired_heading = degrees(
            self.left_encoder_follower.getHeading()
        )
        angle_difference = pf.boundHalfDegrees(
            desired_heading - gyro_heading
        )

        # Wait until pigeon is on board to use this!
        turn = -0.06 * angle_difference
        # turn = 0

        if not (self.left_encoder_follower.isFinished() and self.right_encoder_follower.isFinished()):
            print("Angle Diff", angle_difference)
            robot.chassis.tank_drive(
                -l - turn,
                -r + turn
            )
        else:
            robot.chassis.tank_drive(0, 0)
            print(
                "dist",
                robot.chassis.left_encoder.get_distance(self.WHEEL_DIAMETER)
                )
            self.finish()
