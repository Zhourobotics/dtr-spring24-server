mod state;

use gilrs::{Gilrs, Button, Event, EventType, Axis};
use gilrs::ev::state::AxisData;
use crate::state::ControllerState;

fn main() {
    println!("Hello, world!");

    let mut gilrs = Gilrs::new().unwrap();
    let mut active_gamepad = None;

    let mut state: ControllerState = Default::default();

    loop {
            while let Some(Event { id, event, time }) = gilrs.next_event() {
                if (event == EventType::Connected) {
                    active_gamepad = Some(id);
                    println!("[Console] Connected to controller {}", id);
                }
            }

            // You can also use cached gamepad state
            if let Some(gamepad) = active_gamepad.map(|id| gilrs.gamepad(id)) {
                let leftstick_value = gamepad.axis_data(Axis::LeftStickY).map_or(0.0, |data| data.value());
                state.update(
                    gamepad.is_pressed(Button::East),
                    gamepad.is_pressed(Button::South),
                    gamepad.is_pressed(Button::LeftTrigger2),
                    gamepad.is_pressed(Button::RightTrigger2),
                    gamepad.is_pressed(Button::West),
                    leftstick_value
                );

            }

    }
}
