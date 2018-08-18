#moon transfer
import math
import time
import krpc

conn = krpc.connect(name='Vessel speed')
vessel = conn.space_center.active_vessel

#mun = conn.space_center.bodies["Mun"].velocity(obt_frame)
ap = vessel.auto_pilot
ap.sas = True
ap.sas_mode = ap.sas_mode.prograde
time.sleep(10)
angle = 10
angular_diff = 15

while abs(angle+angular_diff) >= 0.1:
    obt_frame = vessel.orbit.body.non_rotating_reference_frame
    srf_frame = vessel.orbit.body.reference_frame
    mun_orbit = conn.space_center.bodies["Mun"].position(obt_frame)

    vessel_orbit = vessel.position(obt_frame)
    mun_orb= ((mun_orbit[0]**2 + mun_orbit[2]**2)**0.5)

    #deltaV
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    deltav=math.sqrt(mu/a1)*((math.sqrt(2*mun_orb/(mun_orb+a1)))-1)

    angular_diff = math.pi*((1-(1/(2*math.sqrt(2)))*math.sqrt((a1/mun_orb+1)**3)))

    #phase angle
    dot = mun_orbit[0] * vessel_orbit[0] + mun_orbit[2] * vessel_orbit[2]
    det = mun_orbit[0]*vessel_orbit[2] - vessel_orbit[0] *mun_orbit[2]
    angle = math.atan2(det, dot)

    #burn time based on engines
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(deltav/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate

    print("Angle Difference:", abs(angle+angular_diff))
    time.sleep(1)

vessel.control.throttle = 1
time.sleep(burn_time)
vessel.control.throttle = 0
