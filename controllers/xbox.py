from .controller import Controller


class XBox(Controller):
    def __init__(self, channel):
        super().__init__(channel)
        button_verifier = ID_Verifier()
        joystick_verifier = ID_Verifier()

        self.set_drive_forward(joystick_verifier.check(1))
        self.set_drive_turn(joystick_verifier.check(4))

        self.invert_drive_turn()
        # "adam mega cool" - logan, bag night 2019
        self.get_intake_hatch(button_verifier.check(5))
        self.get_drop_hatch(button_verifier.check(4))

        # self.set_rotate_hatch_down(button_verifier.check(7))
        # self.set_rotate_hatch_up(button_verifier.check(8))

        self.set_rotate_cargo_down(button_verifier.check(3))
        self.set_rotate_cargo_up(button_verifier.check(1))

        self.set_shoot(button_verifier.check(6))
        
        self.set_reset_auto_dock(button_verifier.check(9))
        self.set_auto_dock(button_verifier.check(10))

        button_verifier.debug(name="Xbox Buttons")
        joystick_verifier.debug(name="Xbox Axes")