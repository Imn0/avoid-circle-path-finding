from pymavlink import mavutil


master = mavutil.mavlink_connection('udpin:127.0.0.1:14550', autoreconnect=True, retries=10)
master.wait_heartbeat()


master.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, master.target_system,
                        master.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b010111111000), 
                        0, #x 
                        0, #y 
                        -20, 0, 0, 0, 0, 0, 0, 0, 0))