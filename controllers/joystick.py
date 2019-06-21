from .controller import Controller
from checks import ID_Verifier


class Joystick(Controller):
    def __init__(self, channel):
        super().__init__(channel)
        button_verifier = ID_Verifier()
        joystick_verifier = ID_Verifier()

        self.set_drive_forward(joystick_verifier.check(1))
        self.set_drive_turn(joystick_verifier.check(2))

        self.invert_drive_turn()
        # "adam mega cool" - logan, bag night 2019
        self.set_grab_hatch(button_verifier.check(5))
        # self.set_intake_hatch(button_verifier.check(5))
        self.set_drop_hatch(button_verifier.check(6))
        self.set_rotate_cargo_down(button_verifier.check(3))
        self.set_rotate_cargo_up(button_verifier.check(4))

        # self.set_rotate_hatch_down(button_verifier.check(7))
        # self.set_rotate_hatch_up(button_verifier.check(8))
        # self.set_rotate_cargo_down(button_verifier.check(9))
        self.set_reset_auto_dock(button_verifier.check(9))
        self.set_auto_dock(button_verifier.check(11))
        
        self.set_elevator_low(button_verifier.check(8))
        self.set_elevator_mid(button_verifier.check(10))
        self.set_elevator_high(button_verifier.check(12))
        self.set_elevator_cargo_ship(button_verifier.check(7))
        self.set_shift_gears(button_verifier.check(2))

        self.set_shoot(button_verifier.check(1))
        

        button_verifier.debug(name="Joystick Buttons")
        joystick_verifier.debug(name="Joystick Axes")