from wpilib import Joystick
from checks import ID_Verifier


class Controller:
    def __init__(self, channel):
        self.channel = channel
        self.joystick = Joystick(channel)
        self.button_mapping = {}
        self.invert_mapping = {}

    def set_mapping(self, name, joystick_button_number):
        self.button_mapping[name] = joystick_button_number

    def get_mapping(self, name): return self.button_mapping[name]

    def set_invert_mapping(self, name, value):
        self.invert_mapping[name] = value

    def get_joystick_mapping(self, name):
        if name in self.invert_mapping.keys():
            if self.invert_mapping[name]:
                return -1 * self.joystick.getRawAxis(self.get_mapping(name))

        return self.joystick.getRawAxis(self.get_mapping(name))


    def get_button_mapping(self, name):
        return self.joystick.getRawButton(self.get_mapping(name))

    def set_drive_forward(self, value):
        self.set_mapping("drive_forward", value)

    def get_drive_forward(self):
        return self.get_joystick_mapping("drive_forward")

    def invert_drive_forward(self, value=True):
        return self.set_invert_mapping("drive_forward", value)

    def set_drive_turn(self, value):
        self.set_mapping("drive_turn", value)

    def get_drive_turn(self):
        return self.get_joystick_mapping("drive_turn")

    def invert_drive_turn(self, value=True):
        return self.set_invert_mapping("drive_turn", value)

    def set_elevator_low(self, value):
        self.set_mapping("elevator_low", value)

    def get_elevator_low(self):
        return self.get_button_mapping("elevator_low")

    def set_elevator_mid(self, value):
        self.set_mapping("elevator_mid", value)

    def get_elevator_mid(self):
        return self.get_button_mapping("elevator_mid")

    def set_elevator_high(self, value):
        self.set_mapping("elevator_high", value)

    def get_elevator_high(self):
        return self.get_button_mapping("elevator_high")

    def set_elevator_cargo_ship(self, value):
        self.set_mapping("elevator_cargo_ship", value)

    def get_elevator_cargo_ship(self):
        return self.get_button_mapping("elevator_cargo_ship")

    def set_shift_gears(self, value):
        self.set_mapping("shift_gears", value)

    def get_shift_gears(self):
        return self.get_button_mapping("shift_gears")

    def set_intake_hatch(self, value):
        self.set_mapping("intake_hatch", value)

    def get_intake_hatch(self):
        return self.get_button_mapping("intake_hatch")

    def set_grab_hatch(self, value):
        self.set_mapping("grab_hatch", value)

    def get_grab_hatch(self):
        return self.get_button_mapping("grab_hatch")

    def set_drop_hatch(self, value):
        self.set_mapping("drop_hatch", value)

    def get_drop_hatch(self):
        return self.get_button_mapping("drop_hatch")

    def set_hold_hatch(self, value):
        self.set_mapping("hold_hatch", value)

    def get_hold_hatch(self):
        return self.get_button_mapping("hold_hatch")

    def set_close_hatch(self, value):
        self.set_mapping("close_hatch", value)

    def get_close_hatch(self):
        return self.get_button_mapping("close_hatch")

    def set_rotate_hatch_down(self, value):
        self.set_mapping("rotate_hatch_down", value)

    def get_rotate_hatch_down(self):
        return self.get_button_mapping("rotate_hatch_down")

    def set_rotate_hatch_up(self, value):
        self.set_mapping("rotate_hatch_up", value)

    def get_rotate_hatch_up(self):
        return self.get_button_mapping("rotate_hatch_up")

    def set_grab_hatch(self, value):
        self.set_mapping("grab_hatch", value)

    def get_grab_hatch(self):
        return self.get_button_mapping("grab_hatch")

    def set_rotate_cargo_down(self, value):
        self.set_mapping("rotate_cargo_down", value)

    def get_rotate_cargo_down(self):
        return self.get_button_mapping("rotate_cargo_down")

    def set_rotate_cargo_up(self, value):
        self.set_mapping("rotate_cargo_up", value)

    def get_rotate_cargo_up(self):
        return self.get_button_mapping("rotate_cargo_up")

    def set_outtake_hatch(self, value):
        self.set_mapping("outtake_hatch", value)

    def get_outtake_hatch(self):
        return self.get_button_mapping("outtake_hatch")

    def set_shoot(self, value):
        self.set_mapping("shoot", value)

    def get_shoot(self):
        return self.get_button_mapping("shoot")

    def set_intake(self, value):
        self.set_mapping("intake", value)

    def get_intake(self):
        return self.get_button_mapping("intake")

    def set_reset_auto_dock(self, value):
        self.set_mapping("reset_auto_dock", value)

    def get_reset_auto_dock(self):
        return self.get_button_mapping("reset_auto_dock")
        
    def set_auto_dock(self, value):
        self.set_mapping("auto_dock", value)

    def get_auto_dock(self):
        return self.get_button_mapping("auto_dock")