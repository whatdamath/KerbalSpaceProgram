#creates a display

import time
import krpc

conn = krpc.connect(name='User Interface Example')
canvas = conn.ui.stock_canvas

# Get the size of the game window in pixels
screen_size = canvas.rect_transform.size

# Add a panel to contain the UI elements
panel = canvas.add_panel()

# Position the panel on the left of the screen
rect = panel.rect_transform
rect.size = (300, 200)
rect.position = (110-(screen_size[0]/2), 0)

# Add a button to set the throttle to maximum
button = panel.add_button("Full Throttle")
button.rect_transform.position = (0, 20)

# Add some text displaying the total engine thrust
text = panel.add_text("Thrust: 0 kN")
text.rect_transform.position = (0, -20)
text.color = (1, 1, 1)
text.size = 18

text2 = panel.add_text("Speed: 0 m/s")
text2.rect_transform.position = (0, -40)
text2.color = (1, 1, 1)
text2.size = 18

text3 = panel.add_text("Altitude:")
text3.rect_transform.position = (0, -60)
text3.color = (1, 1, 1)
text3.size = 18

# Set up a stream to monitor the throttle button
button_clicked = conn.add_stream(getattr, button, 'clicked')

vessel = conn.space_center.active_vessel
srf_frame = vessel.orbit.body.reference_frame

while True:
    # Handle the throttle button being clicked
    if button_clicked():
        vessel.control.throttle = 1
        button.clicked = False

    # Update the thrust text
    text.content = 'Thrust: %d kN' % (vessel.thrust/1000)
    text2.content = 'Speed: %d m/s' % (vessel.flight(srf_frame).speed)
    text3.content = 'Altitude: %d m' % (vessel.flight(srf_frame).surface_altitude)

    time.sleep(0.1)
