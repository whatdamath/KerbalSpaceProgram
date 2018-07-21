#ultimate takeoff script
#make sure to adjust the stage_2_resources to appropriate stage and change altitude as needed
#this adjust pitch and speed automatically
#you may also want to change dynamic pressure from 4000 to something else
#lastly, adjust the window size and position using rect.size and rect.Position

import math
import time
import krpc

turn_start_altitude = 250
turn_end_altitude = 45000
target_altitude = 100000

conn = krpc.connect(name='Launch into orbit')
canvas = conn.ui.stock_canvas
vessel = conn.space_center.active_vessel
srf_frame = vessel.orbit.body.reference_frame
#screen
screen_size = canvas.rect_transform.size
# Add a panel to contain the UI elements
panel = canvas.add_panel()
# Position the panel on the left of the screen
rect = panel.rect_transform
rect.size = (200, 80)
rect.position = (110-(screen_size[0]/2), 400)

# Add some text displaying the total engine thrust
text = panel.add_text("Dynamic Pr.: 0 kN")
text.rect_transform.position = (0, 20)
text.color = (1, 1, 1)
text.size = 18
text2 = panel.add_text("Speed: 0 m/s")
text2.rect_transform.position = (0, 0)
text2.color = (1, 1, 1)
text2.size = 18
text3 = panel.add_text("Altitude:")
text3.rect_transform.position = (0, -20)
text3.color = (1, 1, 1)
text3.size = 18

# Set up streams for telemetry
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
srf_speed = conn.add_stream(getattr, vessel.flight(srf_frame), 'speed')
dynamic_pressure = conn.add_stream(getattr, vessel.flight(srf_frame), 'dynamic_pressure')
stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
srb_fuel = conn.add_stream(stage_2_resources.amount, 'LiquidFuel')

# Pre-launch setup
vessel.control.sas = False
vessel.control.rcs = False
vessel.control.throttle = 0.5

# Countdown...
print('3...')
time.sleep(1)
print('2...')
time.sleep(1)
print('1...')
time.sleep(1)
print('Launch!')

# Activate the first stage
vessel.control.activate_next_stage()
vessel.auto_pilot.engage()
vessel.auto_pilot.target_pitch_and_heading(90, 90)

# Main ascent loop
srbs_separated = False
turn_angle = 0

while True:

    if dynamic_pressure()/4000 > 1:
        x = 0.5 - (dynamic_pressure()/4000)/5
        vessel.control.throttle = x
    elif dynamic_pressure()/4000 < 0.8:
        vessel.control.throttle = 1
    else:
        x=float((1-dynamic_pressure()/4000)+0.8)
        vessel.control.throttle = x

    #telemetry
    text.content = 'Dynamic Pr.: %d psi' % (dynamic_pressure())
    text2.content = 'Speed: %d m/s' % (srf_speed())
    text3.content = 'Altitude: %d m' % (vessel.flight(srf_frame).surface_altitude)

    # Gravity turn
    if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
        frac = ((altitude() - turn_start_altitude) /
                (turn_end_altitude - turn_start_altitude))
        new_turn_angle = frac * 90

        if abs(new_turn_angle - turn_angle) > 0.5:
            turn_angle = new_turn_angle
            vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, 90)

    # Separate SRBs when finished
    if not srbs_separated:
        if srb_fuel() < 0.1:
            vessel.control.activate_next_stage()
            srbs_separated = True
            time.sleep(0.1)
            #vessel.control.activate_next_stage()
            print('separated')

    # Decrease throttle when approaching target apoapsis
    if apoapsis() > target_altitude*0.9:
        print('Approaching target apoapsis')
        break

    time.sleep(0.1)

# Disable engines when target apoapsis is reached
vessel.control.throttle = 0.25

while apoapsis() < target_altitude:
    text.content = 'Dynamic Pressure: %d psi' % (vessel.thrust/1000)
    text2.content = 'Speed: %d m/s' % (vessel.flight(srf_frame).speed)
    text3.content = 'Altitude: %d m' % (vessel.flight(srf_frame).surface_altitude)
    time.sleep(0.1)
print('Target apoapsis reached')
vessel.control.throttle = 0.0

# Wait until out of atmosphere
print('Coasting out of atmosphere')
while altitude() < 70500:
    text.content = 'Dynamic Pressure: %d psi' % (vessel.thrust/1000)
    text2.content = 'Speed: %d m/s' % (vessel.flight(srf_frame).speed)
    text3.content = 'Altitude: %d m' % (vessel.flight(srf_frame).surface_altitude)
    time.sleep(0.1)

# Plan circularization burn (using vis-viva equation)
print('Planning circularization burn')
mu = vessel.orbit.body.gravitational_parameter
r = vessel.orbit.apoapsis
a1 = vessel.orbit.semi_major_axis
a2 = r
v1 = math.sqrt(mu*((2./r)-(1./a1)))
v2 = math.sqrt(mu*((2./r)-(1./a2)))
delta_v = v2 - v1
node = vessel.control.add_node(
    ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

# Calculate burn time (using rocket equation)
F = vessel.available_thrust
Isp = vessel.specific_impulse * 9.82
m0 = vessel.mass
m1 = m0 / math.exp(delta_v/Isp)
flow_rate = F / Isp
burn_time = (m0 - m1) / flow_rate

# Orientate ship
print('Orientating ship for circularization burn')
vessel.auto_pilot.reference_frame = node.reference_frame
vessel.auto_pilot.target_direction = (0, 1, 0)
vessel.auto_pilot.wait()

# Wait until burn
print('Waiting until circularization burn')
burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
lead_time = 5
conn.space_center.warp_to(burn_ut - lead_time)

# Execute burn
print('Ready to execute burn')
time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
while time_to_apoapsis() - (burn_time/2.) > 0:
    text.content = 'Dynamic Pressure: %d psi' % (vessel.thrust/1000)
    text2.content = 'Speed: %d m/s' % (vessel.flight(srf_frame).speed)
    text3.content = 'Altitude: %d m' % (vessel.flight(srf_frame).surface_altitude)
    time.sleep(0.1)
print('Executing burn')
vessel.control.throttle = 1.0
time.sleep(burn_time - 0.1)
print('Fine tuning')
vessel.control.throttle = 0.05
remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)
while remaining_burn()[1] > 1:
    text.content = 'Dynamic Pressure: %d psi' % (vessel.thrust/1000)
    text2.content = 'Speed: %d m/s' % (vessel.flight(srf_frame).speed)
    text3.content = 'Altitude: %d m' % (vessel.flight(srf_frame).surface_altitude)
    time.sleep(0.1)
vessel.control.throttle = 0.0
node.remove()

print('Launch complete')
