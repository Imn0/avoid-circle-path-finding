from pymavlink import mavutil
import time
import re

# Start a connection listening to a UDP port
master = mavutil.mavlink_connection('udpin:127.0.0.1:14550', autoreconnect=True, retries=10)

print("aaa")

# Make sure the connection is valid
master.wait_heartbeat()

print("aaa")

# master.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, master.target_system,
#                         master.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b010111111000), 
#                         100, #x 
#                         100, #y 
#                         -20, 0, 0, 0, 0, 0, 0, 0, 0))

x_pattern = r'x\s*:\s*([-+]?\d*\.\d+)'
y_pattern = r'y\s*:\s*([-+]?\d*\.\d+)'
while 1:
    msg = master.recv_match(
            type='LOCAL_POSITION_NED', blocking=True)

    msg = str(msg)
    x_match = re.search(x_pattern, msg)
    y_match = re.search(y_pattern, msg)
    if x_match and y_match:
        tmp_x = float(x_match.group(1))
        tmp_y = float(y_match.group(1))
        print(f"{tmp_x},{tmp_y}")


            
