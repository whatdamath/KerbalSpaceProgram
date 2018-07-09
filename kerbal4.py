#TERMINAL VELOCITY CHECKER

import time
import krpc
conn = krpc.connect(name='Vessel speed')
vessel = conn.space_center.active_vessel
srf_frame = vessel.orbit.body.reference_frame

def checker(speed, tvel):
    if speed/tvel > 1:
        x = 0.5 - (speed/tvel)/5
        vessel.control.throttle = x
        print(x)

    elif speed/tvel < 0.5:
        vessel.control.throttle = 1
    else:
        x=float((1-speed/tvel)+0.5)
        vessel.control.throttle = x
        print(x)

while True:
    srf_speed = vessel.flight(srf_frame).speed
    t_vel = vessel.flight(srf_frame).terminal_velocity
    print('Surface speed = %.1f m/s, Terminal velocity = %.1f m/s' %
          (srf_speed, t_vel))
    checker(srf_speed, t_vel)
    time.sleep(1)

#or use streams and dynamic pressure
import time
import krpc
conn = krpc.connect(name='Vessel speed')
vessel = conn.space_center.active_vessel
dynamic_pressure = conn.add_stream(getattr, vessel.flight(srf_frame), 'dynamic_pressure')

while True:
    print(dynamic_pressure())
    time.sleep(1)
