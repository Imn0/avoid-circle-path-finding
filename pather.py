import vertexer
from circle import Circle
from pymavlink import mavutil
import threading
import re
import math
import time
import escaper

pos_x = 0
pos_y = 0
pos_thread_lock = threading.Lock()

def msg_consumer(master: mavutil.mavlink_connection):
    print("msg consumer started")
    global pos_thread_lock
    global pos_x
    global pos_y
    x_pattern = r'x\s*:\s*([-+]?\d*\.\d+)'
    y_pattern = r'y\s*:\s*([-+]?\d*\.\d+)'

    # Use re.search to find the 'x' and 'y' values in the message
    

# Extract the values if matches are found
    

    while True:
        msg = master.recv_match(
        type='LOCAL_POSITION_NED', blocking=True)

        msg = str(msg)
        x_match = re.search(x_pattern, msg)
        y_match = re.search(y_pattern, msg)

        if x_match and y_match:
            tmp_x = float(x_match.group(1))
            tmp_y = float(y_match.group(1))

        # with pos_thread_lock:
            pos_x = tmp_x
            pos_y = tmp_y



def get_curr_pos(master: mavutil.mavlink_connection):
    global pos_thread_lock
    global pos_x
    global pos_y
    with pos_thread_lock:
        curr_pos = (pos_x, pos_y)
    return curr_pos
        


def go_to_xy(x: float, y:float, master: mavutil.mavlink_connection):
    print(f"jolling to {x},{y}")
    master.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, master.target_system,
                        master.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b010111111000), 
                        x, #x 
                        y, #y 
                        -20, 0, 0, 0, 0, 0, 0, 0, 0))

def send_on_path(path, master: mavutil.mavlink_connection):
    for i in range(len(path)):
        go_to_xy(path[i][0], path[i][1], master)
        
        going = True
        while going:
            time.sleep(1)
            pos = get_curr_pos(master)
            if math.dist(pos, (path[i][0], path[i][1]))  < 1:
                going = False

def main():

    master = mavutil.mavlink_connection('udpin:127.0.0.1:14550', autoreconnect=True, retries=10)
    master.wait_heartbeat()

    msg_thread = threading.Thread(target=msg_consumer, args=(master,))
    msg_thread.daemon = True  # This thread will exit when the main program exits
    msg_thread.start()
    initial_count = 0  # Initial count value

   
    # start_x = float(input("start x pos: "))
    # start_y = float(input("start y pos: "))


    # end_x = float(input("end x pos: "))
    # end_y = float(input("end y pos: "))

    # start = (start_x, start_y)
    # end = (end_x, end_y)
    start = (0, 0.0)
    end = (1000.0, 0.0)


    # circle_1 = Circle((50.0, -50.0), 50.0)
    # circle_2 = Circle((200.0, -130.0), 40.0)
    # circle_3 = Circle((150.0, -70.0), 30.0)
    # circle_4 = Circle((300.0, -160.0), 20.0)
    # circle_5 = Circle((301.0, -160.0), 20.0)
    # circle_6 = Circle((290.0, -160.0), 10.0)

    # zones = [circle_1, circle_2, circle_3, circle_4, circle_5, circle_6]
    zones = []

    

    path = vertexer.main(start, end, zones)
    print(f"going on a stroll {path}")
    while True:
        path_thread = threading.Thread(target=send_on_path, args=(path,master,))
        path_thread.daemon = True  # This thread will exit when the main program exits
        path_thread.start()

        center_x = float(input("zone center x pos: "))
        center_y = float(input("zone center y pos: "))
        radius = float(input("zone radius: "))
        zone = Circle((center_x, center_y),radius)
        zones.append(zone) 

        curr_pos = get_curr_pos(master)
        goto = escaper.weg_zur_Freiheit(curr_pos, zones)
        go_to_xy(goto[0], goto[1], master)

        start = get_curr_pos(master)

        path = vertexer.main(start, end, zones)
        print(f"going on a stroll {path}")




if __name__ == "__main__":
    main()
