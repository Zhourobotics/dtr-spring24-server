#[derive(Default)]
pub struct ControllerState {
    forward: bool,
    backward: bool,
    turn_left: bool,
    turn_right: bool,
    killswitch: bool,
    elevator: f32
}

impl ControllerState {
    fn default() -> ControllerState {
        ControllerState {
            forward: false,
            backward: false,
            turn_left: false,
            turn_right: false,
            killswitch: false,
            elevator: 0.0,
        }
    }
    pub fn update(
        &mut self,
        forward_button: bool,
        backward_button: bool,
        left_button: bool,
        right_button: bool,
        killswitch_pressed: bool,
        verticality_stick: f32,
    ) {
        self.forward = forward_button;
        self.backward = backward_button;
        self.turn_left = left_button;
        self.turn_right = right_button;
        self.killswitch = killswitch_pressed;
        self.elevator = verticality_stick;
    }
}