import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import satellite
from satellite import Satellite
from request import Request


MIN_ALTITUDE = satellite.MIN_ALTITUDE
MAX_ALTITUDE = satellite.MAX_ALTITUDE
RANGE_OF_ACTION = satellite.RANGE_OF_ACTION
EARTH_RADIUS = satellite.EARTH_RADIUS


def plot_satellites(satellites, ax):
    '''
    Plot the positions of the satellites.
    
    Required:   satellites (list): A list of Satellite objects.
                ax (matplotlib.axes._subplots.AxesSubplot): The axes to plot the satellites on.
    Returns: None
    '''
    
    
    ax.clear()  # Clear the previous plot
    circle = plt.Circle((0, 0), EARTH_RADIUS, color='blue', fill=False, linestyle='--')
    ax.add_artist(circle)
    alegrete_range = plt.Circle((0, 0), RANGE_OF_ACTION, color='green', fill=False, linestyle='--')
    ax.add_artist(alegrete_range)
    ax.scatter(0, 0, color='blue', label='Alegrete')
    
    for satellite in satellites:
        x = satellite.pos[0]
        y = satellite.pos[1]
        ax.scatter(x, y, color='red', label=f'Satellite {satellite.number}')
        ax.text(x, y, f'Satellite {satellite.number}', fontsize=8, ha='right', va='bottom')
        end_x = x + np.cos(satellite.angle)
        end_y = y + np.sin(satellite.angle)
        if np.sqrt(x**2 + y**2) < RANGE_OF_ACTION:
            ax.arrow(x, y, end_x - x, end_y - y, head_width=5, head_length=1000, fc='red', ec='red')
        else:
            ax.arrow(x, y, end_x - x, end_y - y, head_width=5, head_length=1000, fc='blue', ec='blue')
    
    ax.set_xlabel('X Position (km)')
    ax.set_ylabel('Y Position (km)')
    ax.set_title('Satellite Positions')
    ax.set_aspect('equal')
    ax.set_xlim(-EARTH_RADIUS, EARTH_RADIUS)
    ax.set_ylim(-EARTH_RADIUS, EARTH_RADIUS)
    ax.grid(True)
    plt.pause(0.01)  # Pause to create animation
    


if __name__ == '__main__':
    
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Create a list of satellites
    sats = []
    
    requests = []
    
    number_of_satellites = 70
    
    # Create the satellites and add them to the list
    print(f'Creating {number_of_satellites} satellites...')
    for i in range(number_of_satellites):
        print(f'Creating Satellite {i}')
        x = np.random.randint(-5000, 5000)
        y = np.random.randint(-5000, 5000)
        angle = np.random.uniform(0, 2*np.pi)
        altitude = np.random.randint(MIN_ALTITUDE, MAX_ALTITUDE)
        sat = Satellite(i, altitude, x, y, angle)
        sats.append(sat)
    print('Satellites created!')
    
    # Move the satellites a random amount
    print('Moving the satellites random amounts...')
    for sat in sats:
        sat.move_amount(np.random.randint(0, sat.orbit_circumference))
    print('Satellites moved!')

    # Move the satellites for 1000 iterations
    print('Moving the satellites for 1000 iterations...')
    for i in range(100000):
        print(f'Iteration {i+1}')
        plot_satellites(sats, ax)
        for sat in sats:
            if sat.usable and (sat.capacity < sat.initial_capacity):
                #print(f'Satellite {sat.number}: \nCircumference: {sat.orbit_circumference} km\nx = {sat.x_pos} km\ny = {sat.y_pos} km\nAmount Moved: {sat.amount_moved} km\nOrbit Circumference: {sat.orbit_circumference}\nTime in Range: {sat.time_in_range} seconds\nCapacity: {sat.capacity}')
                if sat.in_range():
                    print("##########################################")
                    print(f'Satellite {sat.number} is in range!')
                    req = next((x for x in requests if x.satellite == sat), None)
                    req.reduce_execution_time()
                    if req.done:
                        print('Solicitation done!')
                        print(f'Releasing satellite {sat.number}...')
                        sat.release_capacity(req.processing_capacity)
                        req.release_satellite()
                        print(f'Satellite {sat.number} released!')
                    else:
                        print(f'Solicitation {req.name}: Time left: {req.time_needed}')
                    print('##########################################')
                                
            sat.move()
        
        rand = np.random.randint(0, 100)
        print('Checking if a event will happen...')
        if rand < 10:
            print('A new solicitation has arrived!')
            proccess = np.random.randint(0, 100)
            time_needed = 60
            req = Request(i, proccess, time_needed)
            print(f'Solicitation {i}: Processing Capacity needed: {proccess} Time needed: {time_needed}')
            print('Checking if there is a satellite available...')
            best_sat = None
            best_distance = sys.float_info.max
            for sat in sats:
                #print(f'Best distance: {best_distance}')
                if sat.usable and sat.capacity >= proccess and sat.time_in_range >= time_needed:
                    print(f'Satellite {sat.number} is available!')
                    print(f'Checking if satellite {sat.number} is the best option...')
                    distance_to_range = sat.distance_to_range()
                    if distance_to_range < best_distance:
                        best_sat = sat
                        best_distance = distance_to_range
                    
            if best_sat is not None:
                print(f'Satellite {best_sat.number} is the best option!')
                print(f'Assigning satellite {best_sat.number} to solicitation {i}')
                best_sat.reserve_capacity(req.processing_capacity)
                req.assign_satellite(best_sat)
                print(f'Satellite {best_sat.number} assigned to solicitation {i}.\nDistance to range: {best_distance}')
                requests.append(req)
            else:
                print('No satellite could be assigned to the solicitation!')
            
        time.sleep(0.1)
            
            
    plt.show()  