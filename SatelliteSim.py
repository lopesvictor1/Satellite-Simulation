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


def plot_satellites(satellites, ax, iteration):
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
    ax.set_title(f'Satellite Positions. Iteration: {iteration}')
    ax.set_aspect('equal')
    ax.set_xlim(-EARTH_RADIUS, EARTH_RADIUS)
    ax.set_ylim(-EARTH_RADIUS, EARTH_RADIUS)
    ax.grid(True)
    plt.pause(0.01)  # Pause to create animation
    

def euclidean_distance(x1, y1, x2, y2):
    '''
    Calculate the Euclidean distance between two points.
    
    Required:   x1 (float): The x-coordinate of the first point.
                y1 (float): The y-coordinate of the first point.
                x2 (float): The x-coordinate of the second point.
                y2 (float): The y-coordinate of the second point.
    Returns: The Euclidean distance between the two points.
    '''
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def search_satellite(satellites, request):
    '''
    Search for a satellite that can fulfill the request.
    
    Required:   satellites (list): A list of Satellite objects.
                request (Request): The request to be fulfilled.
    Returns: The satellite that can fulfill the request.
    '''
    
    if request.satellite is not None:
        base_x = request.satellite.pos[0]
        base_y = request.satellite.pos[1]
        realloc = True
    else:
        base_x = 0
        base_y = 0
        realloc = False
    best_sat = None
    best_distance = sys.float_info.max
    for sat in satellites:
        if sat.usable and sat.capacity >= proccess:
            if realloc:
                if euclidean_distance(sat.pos[0], sat.pos[1], base_x, base_y) < RANGE_OF_ACTION:
                    print(f'Satellite {sat.number} is available!')
                    print(f'Checking if satellite {sat.number} is the best option...')
                    distance_to_range = sat.distance_to_range()
                    if distance_to_range < best_distance:
                        best_sat = sat
                        best_distance = distance_to_range
            else:
                print(f'Satellite {sat.number} is available!')
                print(f'Checking if satellite {sat.number} is the best option...')
                distance_to_range = sat.distance_to_range()
                if distance_to_range < best_distance:
                    best_sat = sat
                    best_distance = distance_to_range
    if best_sat is not None:
        print(f'Satellite {best_sat.number} is the best option!')
        print(f'Assigning satellite {best_sat.number} to solicitation {request.name}')
        best_sat.add_process(request)
        request.assign_satellite(best_sat)
        print(f'Satellite {best_sat.number} assigned to solicitation {request.name}.\nDistance to range: {best_distance}')
        return request
    else:
        print('No satellite could be assigned to the solicitation!')
        return None


if __name__ == '__main__':
    
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Create a list of satellites
    sats = []
    
    requests = []
    
    number_of_satellites = 250
    
    # Create the satellites and add them to the list
    print(f'Creating {number_of_satellites} satellites...')
    for i in range(number_of_satellites):
        print(f'Creating Satellite {i}')
        x = np.random.randint(-5000, 5000)
        y = np.random.randint(-5000, 5000)
        #x = np.random.uniform(-RANGE_OF_ACTION, RANGE_OF_ACTION)
        #y = np.random.uniform(-RANGE_OF_ACTION, RANGE_OF_ACTION)
        angle = np.random.uniform(0, 2*np.pi)
        altitude = np.random.randint(MIN_ALTITUDE, MAX_ALTITUDE)
        sat = Satellite(i, altitude, x, y, angle)
        sats.append(sat)
    print('Satellites created!')
    
    print('Usable Satellites:')
    for sat in sats:
        if sat.usable:
            print(f'Satellite {sat.number} is usable!')
    
    # Move the satellites a random amount
    print('Moving the satellites random amounts...')
    for sat in sats:
        sat.move_amount(np.random.randint(0, sat.orbit_circumference))
        #sat.move_amount(25)
    print('Satellites moved!')

    # Move the satellites for 1000 iterations
    print('Moving the satellites for 1000 iterations...')
    for i in range(100000):
        print(f'Iteration {i+1}')
        #plot_satellites(sats, ax, i)
        for sat in sats:
            #print(f'Satellite {sat.number}. Capacity: {sat.capacity}. Initial Capacity: {sat.initial_capacity}. Usable: {sat.usable}. In Range: {sat.in_range()}, Processes: {sat.processes}')
            #print(f'Satellite {sat.number}: \nCircumference: {sat.orbit_circumference} km\nx = {sat.pos[0]} km\ny = {sat.pos[1]} km\nAmount Moved: {sat.amount_moved} km\nOrbit Circumference: {sat.orbit_circumference}\n')
            if sat.usable and (sat.capacity < sat.initial_capacity):
                if sat.in_range():
                    print(f'Satellite {sat.number} is in range!')
                    for proc in sat.processes:
                        proc.reduce_execution_time()
                        if proc.done:
                            print('Solicitation done!')
                            print(f'Releasing satellite {sat.number}...')
                            sat.remove_process(proc)
                            proc.release_satellite()
                            print(f'Satellite {proc.number} released!')
                        else:
                            print(f'Solicitation {proc.name}: Time left: {proc.time_needed}')
                            pass
                    
                    if sat.is_leaving() == True:
                        print(f'Satellite {sat.number} is leaving range!')
                        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                        print(f'Satellite {sat.number} has the processes: {[x.name for x in sat.processes]}')
                        for process in sat.processes:
                            print(f'Searching for a new satellite for solicitation {process.name}...')
                            proc = search_satellite(sats, process)
                            if proc is not None:
                                print(f'Satellite {sat.number} removed from solicitation {proc.name}')
                                process.release_satellite()
                                sat.remove_process(process)
                            else:
                                print(f'Satellite {sat.number} could not be allocated immediately! Waiting for a new satellite...')
                                process.satellite = None
                                proc = search_satellite(sats, process)
                                if proc is not None:
                                    print(f'Satellite {sat.number} removed from solicitation {proc.name}')
                                    print(f'Satellite {sat.number} assigned to solicitation {proc.name}')
                                    process.release_satellite()
                                    sat.remove_process(process)
                                else:
                                    print(f'Satellite {sat.number} could not be allocated! Holding the process...')

                            
                            
                        print(f'Releasing satellite {sat.number}...')
                        print(f'Satellite {sat.number} released!')
                                
            sat.move()
        
        rand = np.random.randint(0, 100)
        print('Checking if a event will happen...')
        if rand < 10:
            print('A new solicitation has arrived!')
            proccess = np.random.randint(0, 100)
            time_needed = 1000
            req = Request(i, proccess, time_needed)
            print(f'Solicitation {i}: Processing Capacity needed: {proccess} Time needed: {time_needed}')
            print('Checking if there is a satellite available...')
            req = search_satellite(sats, req)
            if req is not None:
                requests.append(req)
                print(f'Solicitation {i} added to the list of requests!')
            else:
                print(f'Solicitation {i} could not be added to the list of requests!')
        else:
            print(f'Current Requests: {[r.name for r in requests]}')
            
        time.sleep(2)
            
            
    plt.show()  