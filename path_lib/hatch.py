from .path import *
from hardware.timer import Timer


class GrabHatch(Segment):
    def config(self, robot):
        self.grabbed_hatch = False
        self.timer = Timer()

    def update(self, robot):
        robot.hatch_holder.update()

        # If we havent grabbed the hatch, grab it
        if not self.grabbed_hatch:
            self.grabbed_hatch = True
            robot.hatch_holder.grab()

            self.timer.wait(2) # Set the timer to wait 1 second

        if self.timer.is_done():
            self.finish()


class DropHatch(Segment):
    def config(self, robot):
        self.dropped_hatch = False
        self.timer = Timer()

    def update(self, robot):
        robot.hatch_holder.update()

        # If we havent grabbed the hatch, grab it
        if not self.dropped_hatch:
            self.dropped_hatch = True
            robot.hatch_holder.drop()

            self.timer.wait(2) # Set the timer to wait 1 second

        if self.timer.is_done():
            self.finish()


class TestSegment(Segment):
    def config(self, robot):
        print("Reached test segment!")
        self.finish()