from math import radians

from wpilib import PIDController
from .path import Path, Segment
from .pathfinder import Trajectory
from hardware.timer import Timer
from networktables.util import ntproperty


def sign(n): return -1 if n < 0 else 1


class PIDVisionAlign(Segment):
    def get_pid(self, sd):
        return [
            # float(sd.getNumber("KP", 0.553) * 4),
            # float(sd.getNumber("KI", 0.033) * 4),
            # float(sd.getNumber("KD", 0.073) * 4)
            0.503 * 4,
            0.033 * 4,
            0.073 * 4
        ]

    def config(self, robot):
        self.pid = PIDController(*self.get_pid(robot.dashboard), self.get_disalignment, self.output)
        self.pid.setOutputRange(-1, 1)
        self.pid.enable()
        self.pid.setSetpoint(0)
        self.turn = 0
        self.robot = robot

    def get_disalignment(self):
        return self.robot.dashboard.getNumber("CENTROID", 0.5) - 0.5

    def output(self, n):
        self.turn = n

    def free(self):
        self.pid.free()

    def update(self, robot):
        err = self.pid.getError()
        self.robot.chassis.arcade_drive(-0.6, self.turn)
        print(self.turn)

        print("err", err)

        self.pid.setPID(
            *self.get_pid(robot.dashboard)
        )


class VisionAlign(Segment):
    def config(self, robot):
        print("Starting vision alignment")
    
    def update(self, robot):
        disalignment = abs(robot.dashboard.getNumber("CENTROID", 0.5) - 0.5)
        n = robot.dashboard.getNumber("CENTROID", 0.5) - 0.5

        if disalignment < 0.05:
            print("Finished aligning")
            self.finish()
        elif disalignment < 0.15:
            if n > 0:
                robot.chassis.arcade_drive(0, -0.42)
            elif n < 0:
                robot.chassis.arcade_drive(0, 0.42)
        else:
            if n > 0:
                robot.chassis.arcade_drive(0, -0.6)
            elif n < 0:
                robot.chassis.arcade_drive(0, 0.6)
                

class VisionTrajectory(Trajectory):
    def __init__(self): pass

    def config(self, robot):
        print("Starting vision trajectory")
        super().__init__([
            (0, 0, radians(0)),
            (robot.dashboard.getNumber("DISTANCE_TO_TARGET", 2), 0, radians(0))
        ])
        super().config(robot)


class VisionSlowForward(Segment):
    def config(self, robot):
        print("Starting slow forward")
        self.timer = Timer()

    def update(self, robot):
        self.timer.wait(2)
        
        FORWARD = -0.5

        disalignment = abs(robot.dashboard.getNumber("CENTROID", 0.5) - 0.5)-0.1
        n = robot.dashboard.getNumber("CENTROID", 0.5) - 0.5

        if disalignment < 0.05:
            robot.chassis.arcade_drive(FORWARD, 0)
        elif disalignment < 0.15:
            if n > 0:
                robot.chassis.arcade_drive(FORWARD, -0.4)
            elif n < 0:
                robot.chassis.arcade_drive(FORWARD, 0.4)
        else:
            if n > 0:
                robot.chassis.arcade_drive(FORWARD, -0.6)
            elif n < 0:
                robot.chassis.arcade_drive(FORWARD, 0.6)

        if self.timer.is_done():
            self.finish()


class VisionApproach(Path):
    def __init__(self, robot):
        super().__init__(robot,
            VisionAlign(),
            VisionTrajectory(),
            VisionAlign(),
            VisionSlowForward()
        )
