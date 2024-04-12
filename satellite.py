import numpy as np

MIN_ALTITUDE = 160
MAX_ALTITUDE = 2000
RANGE_OF_ACTION = 1000
EARTH_RADIUS = 6371


class Satellite:
    def __init__(self, number: int, altitude: int, x: int, y: int, angle: float):
        self.number = number
        self.altitude = altitude
        self.angle = angle
        self.pos = (x, y)
        self.pos_edge = (0, 0)
        self.pos_range = (0, 0)
        self.speed = 27000/3600
        self.orbit_circumference = self.define_orbit_circumference()
        self.distance_to_inverse_edge = self.define_distance_to_inverse_edge()
        self.amount_moved = self.distance_to_inverse_edge
        self.usable = self.define_usable()
        self.time_in_range = self.define_time_in_range()
        self.pos_end = self.define_end_pos()
        self.status = self.define_status()

        self.initial_capacity = 100
        self.capacity = 100
        
    
    def define_orbit_circumference(self):
        '''
        Define the circumference of the orbit based on the altitude of the satellite.
        
        Required: self.altitude (int): The altitude of the satellite in km.
        Returns: orbit_circumference (float): The circumference of the orbit in km.
        '''
        
        orbit_circumference = 2 * np.pi * (self.altitude + EARTH_RADIUS)
        return orbit_circumference
    
    def define_distance_to_inverse_edge(self):
        '''
        Define the distance to the inverse edge of the orbit.
        
        Required:   self.angle (float): The angle of the satellite in radians.
                    self.x_pos (int): The x position of the satellite in km.
                    self.y_pos (int): The y position of the satellite in km.
        Returns: distance_to_inverse_edge (float): The distance to the inverse edge of the orbit in km.
        '''
        distance_to_inverse_edge = 0
        inverse_angle = self.angle - np.pi
        delta_x = self.pos[0]
        delta_y = self.pos[1]
        while np.sqrt(delta_x**2 + delta_y**2) < EARTH_RADIUS:
            delta_x += 1 * np.cos(inverse_angle)
            delta_y += 1 * np.sin(inverse_angle)
            distance_to_inverse_edge += 1
        
        self.pos_edge = (delta_x, delta_y)
        return distance_to_inverse_edge    
    
    def define_usable(self):
        '''
        Define if the satellite is usable (i.e. if it passes through the range of action).
        
        Required:   self.x_pos_edge (int): The x position of the edge of the satellite in km.
                    self.y_pos_edge (int): The y position of the edge of the satellite in km.
        Returns: usable (bool): True if the satellite is usable, False otherwise.
        '''
        usable = False
        delta_x = self.pos_edge[0]
        delta_y = self.pos_edge[1]
        moved = 0
        while moved < EARTH_RADIUS:
            delta_x += 1 * np.cos(self.angle)
            delta_y += 1 * np.sin(self.angle)
            moved += 1
            if np.sqrt(delta_x**2 + delta_y**2) < RANGE_OF_ACTION:
                usable = True
                break
        return usable
    
    def define_time_in_range(self):
        '''
        Calculate the time the satellite is in range of the action.
        
        Required:   self.x_pos (int): The x position of the satellite in km.
                    self.y_pos (int): The y position of the satellite in km.
                    self.angle (float): The angle of the satellite in radians.
        Returns:    time_in_range (float): The time the satellite is in range of the action in seconds.
                    self.x_range (int): The x position of the edge of the range of the satellite in km.
                    self.y_range (int): The y position of the edge of the range of the satellite in km.
        '''
        delta_x = self.pos_edge[0]
        delta_y = self.pos_edge[1]
        time_in_range = 0
        entered = False
        if self.usable == False:
            return 0
        else:
            while entered == False:
                delta_x += 1 * np.cos(self.angle)
                delta_y += 1 * np.sin(self.angle)
                if np.sqrt(delta_x**2 + delta_y**2) < RANGE_OF_ACTION:
                    entered = True
                    break
                
            self.pos_range = (delta_x, delta_y)
            
            while np.sqrt(delta_x**2 + delta_y**2) < RANGE_OF_ACTION:
                delta_x += 1 * np.cos(self.angle)
                delta_y += 1 * np.sin(self.angle)
                time_in_range += 1
                
            return time_in_range

    def define_end_pos(self):
        '''
        Define the end position of the satellite.
        
        Required:   self.x_pos (int): The x position of the satellite in km.
                    self.y_pos (int): The y position of the satellite in km.
                    self.angle (float): The angle of the satellite in radians.
        Returns:    end_pos (tuple): The end position of the satellite in km.
        '''
        delta_x = self.pos_edge[0]
        delta_y = self.pos_edge[1]
        delta_orbit = self.orbit_circumference
        while np.sqrt(delta_x**2 + delta_y**2) < delta_orbit:
            delta_x += 1 * np.cos(self.angle)
            delta_y += 1 * np.sin(self.angle)
            
        return (delta_x, delta_y)
    
    def define_status(self):
        '''
        Define the status of the satellite. 'Away' if is moving away from the range,
                                            'In Range' if is in range of the action,
                                            'Approaching' if is moving towards the range.
                                            'None" if is not usable.
        
        Required:   self.x_pos (int): The x position of the satellite in km.
                    self.y_pos (int): The y position of the satellite in km.
                    self.angle (float): The angle of the satellite in radians.
        Returns:    status (str): The status of the satellite.
        '''
        
        if self.usable == False:
            return 'None'
        elif self.in_range():
            return 'In Range'
        else:
            delta_x = self.pos[0]
            delta_y = self.pos[1]
            distance_to_range = np.sqrt((delta_x - self.pos_range[0])**2 + (delta_y - self.pos_range[1])**2)
            
            delta_x += 1 * np.cos(self.angle)
            delta_y += 1 * np.sin(self.angle)
            
            if np.sqrt((delta_x - self.pos_range[0])**2 + (delta_y - self.pos_range[1])**2) < distance_to_range:
                return 'Approaching'
            else:
                return 'Away'
            
        

    def move(self):
        '''
        Move the satellite along its orbit by the speed of the satellite.
        
        Required:   self.speed (float): The speed of the satellite in km/s.
                    self.angle (float): The angle of the satellite in radians.
                    self.x_pos (int): The x position of the satellite in km.
                    self.y_pos (int): The y position of the satellite in km.
                    self.orbit_circumference (float): The circumference of the orbit in km.
                    self.amount_moved (float): The amount of the orbit that has been moved in km.
                    
        Returns: Updates the x_pos, y_pos, and amount_moved attributes of the satellite.
        '''
        speed = 0
        
        if self.amount_moved + self.speed >= self.orbit_circumference:
            speed = self.orbit_circumference - self.amount_moved
            self.amount_moved = 0
            self.pos = self.pos_edge
            self.status = 'Approaching'
        else:
            speed = self.speed        
        # Calculate the change in position based on the fixed angle
        delta_x = speed * np.cos(self.angle)
        delta_y = speed * np.sin(self.angle)
        self.status = self.define_status()
        
        # Update the position
        self.pos += (delta_x, delta_y)
            
        self.amount_moved += speed
        
    def move_amount(self, amount):
        '''
        Move the satellite along its orbit by a specified amount.
        
        Required:   amount (float): The amount to move the satellite in km.
                    self.angle (float): The angle of the satellite in radians.
                    self.x_pos (int): The x position of the satellite in km.
                    self.y_pos (int): The y position of the satellite in km.
                    self.orbit_circumference (float): The circumference of the orbit in km.
                    self.amount_moved (float): The amount of the orbit that has been moved in km.
                    
        Returns: Updates the x_pos, y_pos, and amount_moved attributes of the satellite.
        '''
        speed = 0
        
        if self.amount_moved + amount >= self.orbit_circumference:
            speed = self.orbit_circumference - self.amount_moved
            self.amount_moved = 0
            self.pos = self.pos_edge
        else:
            speed = amount        
        # Calculate the change in position based on the fixed angle
        delta_x = speed * np.cos(self.angle)
        delta_y = speed * np.sin(self.angle)
        
        # Update the position
        self.pos += (delta_x, delta_y)
            
        self.amount_moved += speed

    def distance_to_range(self):
        '''
        Calculate the distance to the range of the action.
        
        Required:   self.x_pos (int): The x position of the satellite in km.
                    self.y_pos (int): The y position of the satellite in km.
        Returns: distance_to_range (float): The distance to the range of the action in km.
        '''
        if self.status == 'In Range':
            distance_to_range = 0
        elif self.status == 'Approaching':
            distance_to_range = np.sqrt((self.pos[0] - self.pos_range[0])**2 + (self.pos[1] - self.pos_range[1])**2)
        else:
            distance_to_end = np.sqrt((self.pos[0] - self.pos_end[0])**2 + (self.pos[1] - self.pos_end[1])**2)
            distance_from_start_to_range = np.sqrt((self.pos_edge[0] - self.pos_range[0])**2 + (self.pos_edge[1] - self.pos_range[1])**2)
            distance_to_range = distance_to_end + distance_from_start_to_range
        return distance_to_range

    def reserve_capacity(self, capacity):
        '''
        Reserve the capacity of the satellite.
        
        Required: capacity (int): The capacity to reserve.
        Returns: Updates the capacidade attribute of the satellite.
        '''
        self.capacity -= capacity
        
    def release_capacity(self, capacity):
        '''
        Release the capacity of the satellite.
        
        Required: capacity (int): The capacity to release.
        Returns: Updates the capacidade attribute of the satellite.
        '''
        self.capacity += capacity
        
    
    def in_range(self):
        '''
        Check if the satellite is in range of the action.
        
        Required:   self.x_pos (int): The x position of the satellite in km.
                    self.y_pos (int): The y position of the satellite in km.
        Returns: in_range (bool): True if the satellite is in range of the action, False otherwise.
        '''
        in_range = False
        if np.sqrt((self.pos[0])**2 + (self.pos[1])**2) < RANGE_OF_ACTION:
            in_range = True
        return in_range