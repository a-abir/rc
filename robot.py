# from small_vision import Image
# from path_lib import Path, Segment
from networktables.util import ntproperty

from wpilib import run, TimedRobot
from networktables import NetworkTables

from checks import ID_Verifier
from hardware import Talon, Elevator, Intake, Chassis
from hardware import HatchFloorGrabber, HatchHolder, CargoGrabber

from math import radians
from path_lib import Path, PigeonApproach, PIDVisionAlign, VisionApproach, Trajectory, GrabHatch, DropHatch, TestSegment, LEFT_ROCKET_FRONT

from controllers import Joystick

NetworkTables.initialize()


MotorId = ID_Verifier()
PneumaticID = ID_Verifier()


class ID:
    class Drive:
        # class LowGear:
        #     channel = PneumaticID.check(0)

        # class HighGear:
        #     channel = PneumaticID.check(1)
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

    # class Intake:
    #     front = MotorId.check(3)
    #     back = MotorId.check(4)

    # class Elevator:
    #     master = MotorId.check(11)
    #     slaves = [MotorId.check(10)]

    # this is flipped with intake
    class Intake:
        front = MotorId.check(10)
        back = MotorId.check(11)
        
    class Elevator:
        master = MotorId.check(4)
        slaves = [MotorId.check(3)]

    class HatchFloorGrabber:
        rotate = MotorId.check(2)
        intake = MotorId.check(1)

    class HatchHolder:
        # extend_port = PneumaticID.check(2)
        # retract_port = PneumaticID.check(3)
        # open_port = PneumaticID.check(4)
        # close_port = PneumaticID.check(5)

        # extend_port = PneumaticID.check(4)
        # retract_port = PneumaticID.check(5)
        # open_port = PneumaticID.check(2)
        # close_port = PneumaticID.check(3)

        extend_port = PneumaticID.check(2)
        retract_port = PneumaticID.check(3)
        open_port = PneumaticID.check(4)
        close_port = PneumaticID.check(5)

    class CargoGrabber:
        rotate = MotorId.check(8)
        intake = MotorId.check(9)


MotorId.debug(name="Motor IDs")
PneumaticID.debug(name="Pneumatic IDs")


class Finn(TimedRobot):
    elevator_distance = ntproperty("/SmartDashboard/elevator_distance", defaultValue=0.5, writeDefault=True)


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


    dashboard = NetworkTables.getTable("SmartDashboard")


    def robotInit(self):
        print("hello world")
        self.joystick = Joystick(0)
        self.path = None
        self.chassis.reset_sensors()
        self.elevator.reset_sensors()

    def autonomousInit(self):
        try:
            self.chassis.reset_sensors()
            self.elevator.reset_sensors()
            self.elevator.low()
            self.teleopInit()
        except Exception as e: print(e)

    def autonomousPeriodic(self): self.teleopPeriodic()

    def teleopPeriodic(self):
        try:
            # chassis
            self.chassis.update()
            self.chassis.arcade_drive(
                self.joystick.get_drive_forward(),
                self.joystick.get_drive_turn() * 0.7
            )

            if self.joystick.get_shift_gears():
                self.chassis.shift()
            

            # hatch floor grabber
            # self.hatch_floor_grabber.update()
            # self.hatch_floor_grabber.hold_up()


            # hatch holder
            self.hatch_holder.update()
            if self.joystick.get_intake_hatch():
                print("intaking")
                self.hatch_holder.intake()
            elif self.joystick.get_drop_hatch():
                print("dropping")
                self.hatch_holder.drop()
            elif self.hatch_holder.is_intaking():
                print("holding")
                self.hatch_holder.hold()


            # cargo grabber
            self.cargo_grabber.update()
            if self.joystick.get_rotate_cargo_down():
                print("getting cargo")
                self.cargo_grabber.get_cargo()
                self.elevator.zero()
            elif self.joystick.get_rotate_cargo_up():
                self.cargo_grabber.stop_getting_cargo()


            # intake
            self.intake.update()
            if self.joystick.get_shoot():
                self.intake.shoot()
            elif not self.cargo_grabber.is_stopping():
                self.intake.slow_intake()
            else:
                self.intake.idle()

            # elevator
            self.elevator.update()
            if self.joystick.get_elevator_low():
                self.elevator.low()
            elif self.joystick.get_elevator_mid():
                self.elevator.mid()
            elif self.joystick.get_elevator_high():
                self.elevator.high()
            elif self.joystick.get_elevator_cargo_ship():
                self.elevator.cargo_ship()
            # if self.joystick.get_elevator_low():
            #     self.elevator.down()
            #     print("down")
            # elif self.joystick.get_elevator_high():
            #     self.elevator.up()
            #     print("up")
            # else:
            #     self.elevator.stop()
            #     print("stopping")
            

            # print(self.elevator.is_going_up())
            print(
                "Elevator position in feet:",
                self.elevator.get_actual_position() / 3.14,
                "Output voltage", self.elevator.master_talon.getMotorOutputVoltage()
            )

        except Exception as e: print(e)

if __name__ == "__main__":
    run(Finn)



