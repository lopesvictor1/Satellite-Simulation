import numpy as np
import matplotlib.pyplot as plt
import time


MIN_ALTITUDE = 160
MAX_ALTITUDE = 2000
RANGE_OF_ACTION = 1000
EARTH_RADIUS = 6371


class Satellite:
    def __init__(self, number: int, altitude: int, status: str, x: int, y: int, angle: float):
        self.number = number
        self.altitude = altitude
        self.status = status
        self.speed = 27000/50
        self.angle = y
        self.x_pos = x
        self.y_pos = y
        self.x_pos_edge = 0
        self.y_pos_edge = 0
        self.orbit_circumference = self.define_orbit_circumference()
        self.distance_to_inverse_edge = self.define_distance_to_inverse_edge()
        self.amount_moved = self.distance_to_inverse_edge
        self.capacidade = 10
        self.reserved = False
        
    
    def define_orbit_circumference(self):
        orbit_circumference = 2 * np.pi * (self.altitude + EARTH_RADIUS)
        return orbit_circumference
    
    def define_distance_to_inverse_edge(self):
        distance_to_inverse_edge = 0
        inverse_angle = self.angle - np.pi
        delta_x = self.x_pos
        delta_y = self.y_pos
        while np.sqrt(delta_x**2 + delta_y**2) < EARTH_RADIUS:
            delta_x += 1 * np.cos(inverse_angle)
            delta_y += 1 * np.sin(inverse_angle)
            distance_to_inverse_edge += 1
        
        self.x_pos_edge = delta_x
        self.y_pos_edge = delta_y
        return distance_to_inverse_edge    

    def move(self):
        speed = 0
        
        if self.amount_moved + self.speed >= self.orbit_circumference:
            speed = self.orbit_circumference - self.amount_moved
            self.amount_moved = 0
            self.x_pos = self.x_pos_edge
            self.y_pos = self.y_pos_edge
        else:
            speed = self.speed        
        # Calculate the change in position based on the fixed angle
        delta_x = speed * np.cos(self.angle)
        delta_y = speed * np.sin(self.angle)
        
        # Update the position
        self.x_pos += delta_x
        self.y_pos += delta_y
            
        self.amount_moved += speed
        
    def move_amount(self, amount):
        speed = 0
        
        if self.amount_moved + amount >= self.orbit_circumference:
            speed = self.orbit_circumference - self.amount_moved
            self.amount_moved = 0
            self.x_pos = self.x_pos_edge
            self.y_pos = self.y_pos_edge
        else:
            speed = amount        
        # Calculate the change in position based on the fixed angle
        delta_x = speed * np.cos(self.angle)
        delta_y = speed * np.sin(self.angle)
        
        # Update the position
        self.x_pos += delta_x
        self.y_pos += delta_y
            
        self.amount_moved += speed

def plot_satellites(satellites, ax):
    ax.clear()  # Clear the previous plot
    circle = plt.Circle((0, 0), EARTH_RADIUS, color='blue', fill=False, linestyle='--')
    ax.add_artist(circle)
    alegrete_range = plt.Circle((0, 0), RANGE_OF_ACTION, color='green', fill=False, linestyle='--')
    ax.add_artist(alegrete_range)
    ax.scatter(0, 0, color='blue', label='Alegrete')
    
    for satellite in satellites:
        x = satellite.x_pos
        y = satellite.y_pos
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
    plt.savefig(f'satellite_positions{satellites[0].x_pos}.png')
    plt.pause(0.01)  # Pause to create animation
    

fig, ax = plt.subplots(figsize=(10, 10))

sats = []

for i in range(200):
    x = np.random.randint(-5000, 5000)
    y = np.random.randint(-5000, 5000)
    angle = np.random.uniform(0, 2*np.pi)
    altitude = np.random.randint(MIN_ALTITUDE, MAX_ALTITUDE)
    sat = Satellite(i, altitude, 'active', x, y, angle)
    sats.append(sat)
    
for i in sats:
    i.move_amount(np.random.randint(0, 35000))

for i in range(10):
    plot_satellites(sats, ax)
    for sat in sats:
        print(f'X = {sat.x_pos}, Y = {sat.y_pos}')
        print(f'Distance to Inverse Edge: {sat.distance_to_inverse_edge} km\n')
        print(f'Circumference: {sat.orbit_circumference} km\n')
        print(f'Amount Moved: {sat.amount_moved} km\n')
        print("\n")
        sat.move()
plt.show()  