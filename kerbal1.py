import krpc

conn = krpc.connect(name='Vessel')
vessel = conn.space_center.active_vessel

flight_info = vessel.flight()
print(flight_info.mean_altitude)
refframe =vessel.orbit.body.reference_frame
print(vessel.position(reframe))





#####
#part 2
import krpc
import time
conn = krpc.connect(name='Vessel')
vessel = conn.space_center.active_vessel

vessel.auto_pilot.target_pitch_and_heading(90,90)
vessel.auto_pilot.engage()
vessel.control.throttle=1
time.sleep(1)
print("Launch!")
vessel.control.activate_next_stage()

#####
#part 3 staging

#sub orbital flight
import krpc
import time
conn = krpc.connect()
vessel = conn.space_center.active_vessel
vessel.auto_pilot.target_pitch_and_heading(90, 90)
vessel.auto_pilot.engage()
vessel.control.throttle = 1
time.sleep(1)
print('Launch!')
vessel.control.activate_next_stage()

fuel_amount = conn.get_call(vessel.resources_in_decouple_stage(1, cumulative = False).amount, 'LiquidFuel')
expr = conn.krpc.Expression.less_than(
    conn.krpc.Expression.call(fuel_amount),
    conn.krpc.Expression.constant_float(0.1))
event = conn.krpc.add_event(expr)
fuelz = vessel.resources_in_decouple_stage(1, cumulative = False).amount('LiquidFuel')

while fuelz > 1.0:
    print(vessel.resources_in_decouple_stage(1, cumulative = False).amount('LiquidFuel'))
    time.sleep(1)
    fuelz = vessel.resources_in_decouple_stage(1, cumulative = False).amount('LiquidFuel')


print('Booster separation')
vessel.control.activate_next_stage()
time.sleep(1)
vessel.control.activate_next_stage()
