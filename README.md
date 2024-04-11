# Satellite Simulation Project

This project simulates the movement of satellites around the Earth within a specified orbit range. It utilizes Python with NumPy and Matplotlib libraries to create a visual representation of satellite movements.

## Features

- Simulates the movement of multiple satellites around the Earth.
- Satellites have adjustable altitudes, speeds, and initial positions.
- Visualizes satellite positions in real-time.
- Calculates distances to the inverse edge of the orbit range.

## Example
This is an frame of the execution of the code. The arrows next to the Satellites points towards its next movement (his 'angle'). Satellites with red arrows are within the range of action.

The blue circle is the cartesian projection of Earth's border, while the green circle is the range where the blue point can access the transiting satellites.

![Satellite Simulation](/Plots/Satellites_Example.png)

## Requirements

- Python 3.x
- NumPy
- Matplotlib

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/satellite-simulation.git
    ```

2. Install the required dependencies:

    ```bash
    pip install numpy matplotlib
    ```

## Usage

1. Navigate to the project directory:

    ```bash
    cd satellite-simulation
    ```

2. Run the main script:

    ```bash
    python satellite_simulation.py
    ```

3. Follow the on-screen instructions to interact with the simulation.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
