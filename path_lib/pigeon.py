from math import radians, degrees, sin, cos

from .path import Path, Segment
from .pathfinder import Trajectory
from hardware.timer import Timer


LEFT_ROCKET_FRONT = 28.56 # degrees


def sign(n): return -1 if n < 0 else 1


class PigeonTrajectory(Trajectory):
    def __init__(self, target_angle=0):
        self.target_angle = radians(target_angle)

    def config(self, robot):
        print("Starting pigeon trajectory")
        current_angle = radians(robot.chassis.gyro.getAngle())

        distance_to_target = None
        angle1 = None
        angle2 = None

        # target_info[0] = timestamp of image in seconds.
        # target_info[1] = success (1.0) OR failure (0.0)
        # target_info[2] = mode (1=driver, 2=rrtarget)
        # target_info[3] = distance to target (inches)
        # target_info[4] = angle1 to target (radians) -- angle displacement of robot to target
        # target_info[5] = angle2 of target (radians) -- angle displacement of target to robot
        target_info = robot.dashboard.getNumberArray("vision/target_info", None)
        if target_info:
            distance_to_target = target_info[3]
            angle1 = target_info[4]
            angle2 = target_info[5]
        
            d = (distance_to_target+9)/12
            pathfinder_angle = radians(90) - abs(angle2)


            pathfinder_y = d * sign(angle1) * cos(pathfinder_angle)
            pathfinder_x = d * sin(pathfinder_angle)

            # print(pathfinder_y, pathfinder_x)

            final_angle = sign(angle1) * (radians(90) - abs(pathfinder_angle))


            # print("path ang", )
            # super().__init__([
            #     (0, 0, 0),
            #     (pathfinder_x, pathfinder_y+0.1, final_angle),
            # ])
            
            super().__init__([
                (0, 0, 0),
                (pathfinder_x, -pathfinder_y, self.target_angle - current_angle),
            ])

            super().config(robot)
            # self.finish()

        else:
            print("Couldnt read target info")
            self.finish()


class PigeonApproach(Path):
    def __init__(self, robot, target_angle):
        super().__init__(robot,
            PigeonTrajectory(target_angle)
        )


