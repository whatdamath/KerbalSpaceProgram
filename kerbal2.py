#VELOCITY

import time
import krpc

conn = krpc.connect(name='Vessel speed')
vessel = conn.space_center.active_vessel
obt_frame = vessel.orbit.body.non_rotating_reference_frame
srf_frame = vessel.orbit.body.reference_frame

while True:
    obt_speed = vessel.flight(obt_frame).speed
    srf_speed = vessel.flight(srf_frame).speed
    t_vel = vessel.flight(srf_frame).terminal_velocity
    altitude = vessel.flight(srf_frame).mean_altitude
    print('Orbital speed = %.1f m/s, Surface speed = %.1f m/s, Terminal velocity = %.1f m/s, Altitude = %.1f m' %
          (obt_speed, srf_speed, t_vel, altitude))
    time.sleep(1)


#or us this one instead

import time
import krpc

conn = krpc.connect(name='Vessel speed')
vessel = conn.space_center.active_vessel

altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
velocity = conn.add_stream(getattr, vessel.flight(), "speed")

while True:
    print (altitude(),velocity())
    time.sleep(1)
