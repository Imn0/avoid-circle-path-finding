from pymavlink import mavutil

# Start a connection listening to a UDP port
master = mavutil.mavlink_connection('udpin:127.0.0.1:14550', autoreconnect=True, retries=10)

print("aaa")

# Make sure the connection is valid
master.wait_heartbeat()

print("aaa")

master.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, master.target_system,
                        master.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b010111111000), 40, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0))