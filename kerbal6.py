#landing script for krpc and Kerbal Space Program
import math
import time
import krpc

conn = krpc.connect(name='Vessel speed')
vessel = conn.space_center.active_vessel
obt_frame = vessel.orbit.body.non_rotating_reference_frame
srf_frame = vessel.orbit.body.reference_frame
orb_speed = conn.add_stream(getattr, vessel.flight(obt_frame), 'speed')
altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
srf_speed = conn.add_stream(getattr, vessel.flight(srf_frame), 'speed')

long = conn.add_stream(getattr, vessel.flight(obt_frame), 'longitude')

vessel.control.speed_mode = vessel.control.speed_mode.surface
ap = vessel.auto_pilot
ap.sas = True
ap.sas_mode = ap.sas_mode.retrograde
time.sleep(1)

#angle = 66
angle = 62
position = 0
ksc_loc = (1.301492-angle*math.pi/180)
while abs(position - ksc_loc) > 0.01:
    position = (long()+180)*math.pi/180
    print(abs(position - ksc_loc))
    time.sleep(1)

time.sleep(1)
while (vessel.orbit.periapsis_altitude > 0):
        vessel.control.throttle = 1.0
vessel.control.throttle = 0.0

while altitude() > 50000:
    pass
while (orb_speed() > 1500):
        vessel.control.throttle = 1.0
vessel.control.throttle = 0.0

while altitude() > 10000:
    pass
while (srf_speed() > 500):
        vessel.control.throttle = 1.0
vessel.control.throttle = 0.0
while altitude() > 2000:
    pass
while (srf_speed() > 200):
        vessel.control.throttle = 1.0
vessel.control.throttle = 0.0
while altitude() > 1200:
    pass
while altitude() > 50:
    if srf_speed() > altitude()/5:
        vessel.control.throttle = 0.95
    elif srf_speed() > altitude()/10:
        vessel.control.throttle = 0.1
    elif srf_speed() > altitude()/15:
        vessel.control.throttle = 0

while altitude() > 2:
    if srf_speed() > 7:
        vessel.control.throttle = 0.5
    else:
        vessel.control.throttle = 0
vessel.control.throttle = 0
