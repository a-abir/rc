# frc-6517
6517 FRC robot code

## hardware
---

The `hardware` package in this project contains all the abstractions we use on our bot. It implements gyro, encoder, limit switch objects as well as entire subsystems such as our cargo intake and hatch holder. 

## controllers
---

The `controller` package abstracts the Joystick object in wpilib, and allows us to much more easily port the controls of our robot to different devices. 

## remote_path
---

`remote_path` is a library that lets us generate trajectories in pathfinder remotely.

[The path_lib repo can be found here](https://github.com/adam-mcdaniel/auto-bot)

## path_lib
---

`path_lib` is a library that lets us make a state-machine that controls our bot over a Path. It allows us to easily stitch Path segments together, into a complicated set of movements.

[The path_lib repo can be found here](https://github.com/adam-mcdaniel/auto-bot)

## small_vision
---

`small_vision` is a rather small library of abstractions on top of OpenCV. It allows us to write vision processing software that normally takes ~60 lines of code in 15 or less.

Because it's very light, you can just convert an image to an opencv image if you want to do some more low level computations that cant be done with small vision.

[The small_vision repo can be found here](https://github.com/adam-mcdaniel/small-vision)

## robot.py
---

This file contains our main Robot class. It is the heart of our code, and it's where everything actually happens.

```python
from wpilib import run, TimedRobot
from networktables import NetworkTables

from checks import ID_Verifier
from hardware import Talon, Elevator, Intake, Chassis
from hardware import HatchFloorGrabber, HatchHolder, CargoGrabber


from controllers import Joystick

NetworkTables.initialize()
sd = NetworkTables.getTable("SmartDashboard")


MotorId = ID_Verifier()
PneumaticID = ID_Verifier()


class ID:
    class Drive:
        class LowGear:
            channel = PneumaticID.check(1)

        class HighGear:
            channel = PneumaticID.check(0)

        class Left:
            master = MotorId.check(5)
            slaves = [
                MotorId.check(6),
                MotorId.check(7)
            ]

        class Right:
            master = MotorId.check(12)
            slaves = [
                MotorId.check(13),
                MotorId.check(14)
            ]

    class Intake:
        front = MotorId.check(3)
        back = MotorId.check(4)
    class Elevator:
        master = MotorId.check(10)
        slaves = [MotorId.check(11)]

    class HatchFloorGrabber:
        rotate = MotorId.check(2)
        intake = MotorId.check(1)

    class HatchHolder:
        extend_port = PneumaticID.check(3)
        retract_port = PneumaticID.check(2)
        open_port = PneumaticID.check(5)
        close_port = PneumaticID.check(4)

    class CargoGrabber:
        rotate = MotorId.check(9)
        intake = MotorId.check(8)


MotorId.debug(name="Motor IDs")
PneumaticID.debug(name="Pneumatic IDs")


class Finn(TimedRobot):
    chassis = Chassis(
                ID.Drive.Left.master, ID.Drive.Right.master,
                left_slave_ids=ID.Drive.Left.slaves,
                right_slave_ids=ID.Drive.Right.slaves,
                low_gear_solenoid_port=ID.Drive.LowGear.channel,
                high_gear_solenoid_port=ID.Drive.HighGear.channel
                )

    intake = Intake(ID.Intake.front, ID.Intake.back)

    elevator = Elevator(ID.Elevator.master, ID.Elevator.slaves)

    hatch_floor_grabber = HatchFloorGrabber(
        ID.HatchFloorGrabber.rotate,
        ID.HatchFloorGrabber.intake
    )

    hatch_holder = HatchHolder(
        ID.HatchHolder.extend_port,
        ID.HatchHolder.retract_port,
        ID.HatchHolder.open_port,
        ID.HatchHolder.close_port
    )

    cargo_grabber = CargoGrabber(
        ID.CargoGrabber.rotate,
        ID.CargoGrabber.intake
    )

    subsystems = [
        chassis,
        intake,
        elevator,
        hatch_floor_grabber,
        hatch_holder,
        cargo_grabber
    ]


    def robotInit(self):
        self.joystick = Joystick(0)


    def teleopPeriodic(self):

        # for subsystem in self.subsystems:
        #     subsystem.update()
        self.chassis.update()
        self.chassis.arcade_drive(
            self.joystick.get_drive_forward(),
            self.joystick.get_drive_turn() * 0.7
        )

        # hatch floor grabber
        self.hatch_floor_grabber.update()
        if self.joystick.get_rotate_hatch_up():
            self.hatch_floor_grabber.rotate_up()
        elif self.joystick.get_rotate_hatch_down():
            self.hatch_floor_grabber.rotate_down()
        else:
            self.hatch_floor_grabber.brake_rotate()
        
        if self.joystick.get_grab_hatch():
            self.hatch_floor_grabber.intake()
        elif self.joystick.get_grab_cargo():
            self.hatch_floor_grabber.outtake()
        else:
            self.hatch_floor_grabber.brake_intake()

        # hatch holder
        self.hatch_holder.update()
        if self.joystick.get_grab():
            self.hatch_holder.grab()
        elif self.joystick.get_drop():
            self.hatch_holder.drop()
        elif self.joystick.get_hold():
            self.hatch_holder.hold()
        elif self.joystick.get_close():
            self.hatch_holder.stop()

        # cargo grabber
        self.cargo_grabber.update()
        if self.joystick.get_rotate_cargo_up():
            self.cargo_grabber.rotate_up()
            self.cargo_grabber.intake()
        elif self.joystick.get_rotate_cargo_down():
            self.cargo_grabber.rotate_down()
            self.cargo_grabber.intake()
        else:
            self.cargo_grabber.brake_rotate()
            self.cargo_grabber.brake_intake()

        # # elevator
        # self.elevator.go_to_feet(0)

        # intake
        self.intake.update()
        if self.joystick.get_shoot():
            self.intake.shoot()
        elif self.joystick.get_intake():
            self.intake.intake()
        elif self.joystick.get_rotate_cargo_up():
            self.intake.intake()
        else:
            self.intake.idle()

if __name__ == "__main__":
    run(Finn)
```