#moon landing

import math
import time
import krpc

conn = krpc.connect(name='Vessel Landing')
vessel = conn.space_center.active_vessel
obt_frame = vessel.orbit.body.non_rotating_reference_frame
orb_speed = conn.add_stream(getattr, vessel.flight(obt_frame), 'speed')
altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
#srf_speed = conn.add_stream(getattr, vessel.flight(srf_frame), 'speed')

print ("Deorbiting Vessel...")
vessel.control.speed_mode = vessel.control.speed_mode.surface
ap = vessel.auto_pilot
ap.sas = True
ap.sas_mode = ap.sas_mode.retrograde

while altitude() > 15000:
    pass
while (orb_speed() > 500):
        vessel.control.throttle = 1.0
vessel.control.throttle = 0.0

while altitude() > 7000:
    pass
print("7000 done")
while (orb_speed() > 250):
        vessel.control.throttle = 1.0
vessel.control.throttle = 0.0
while altitude() > 1500:
    pass
print("1500 done")
while (orb_speed() > 100):
        vessel.control.throttle = 1.0
vessel.control.throttle = 0.0
print("pre300")
while altitude() > 300:
    pass
print("300 done")
while altitude() > 50:
    if orb_speed() > 12:
        vessel.control.throttle = 0.5
    else:
        vessel.control.throttle = 0

print("50 done")
while altitude() > 5:
    if orb_speed() > 10:
        vessel.control.throttle = 0.2
    else:
        vessel.control.throttle = 0
vessel.control.throttle = 0

        
