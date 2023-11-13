import math

# Change this constants to test different scenarios
drone_weight = [15.]    # Weight of the drone in kg
drone_length = 1.5      # Diagonal of the drone in m
arm_weight = [6., 8.]       # Weight of the arm in kg
arm_length = [1.1]       # Length of the arm in m
tank_weight = [2.]      # Weight of the tank in kg
tank_length = .5        # Length of the tank in m
max_tilt = 20  # Max tilt angle (degrees)


g = 9.81  # Acceleration due to gravity (m/s^2)


# Define drone part
class Component:
    def __init__(self, name, weight, length, distance):
        self.name = name
        self.weight = weight
        self.length = length
        self.distance = distance

    def get_force(self):
        return self.weight * g
    
    def get_moment(self, cog):
        dist = abs(self.distance - cog)
        return self.get_force() * dist


def calculate_cog(components):
    n = 0
    d = 0

    for component in components:
        n += component.weight * component.distance
        d += component.weight

    return n / d


def get_required_thrust(cog, arm, drone, tank):
    # Calcumate momemt due to arm
    m_arm = arm.get_moment(cog)

    # Calculate moment due to thrust 
    # m_thrust = f_thrust * r_titled
    r_titled = abs(drone.distance - cog) * math.cos(max_tilt)

    # Calculate moment due to weight
    m_drone = drone.get_moment(cog) + tank.get_moment(cog)

    # Equate the moments: m_thrust = m_arm + m_drone
    f_thrust = (m_arm + m_drone) / r_titled

    return f_thrust


# Get the maximum inclination
# Test different scenarios
for d_w in drone_weight:
    for t_w in tank_weight:
        for a_l in arm_length:
            for a_w in arm_weight:
                drone = Component("drone", d_w, drone_length, drone_length/2)
                tank = Component("tank", t_w, tank_length, drone_length/2)
                arm = Component("arm", a_w, a_l, (a_l/2 + drone_length/2))
                components = [drone, tank, arm]

                # Calculate center of gravity
                cog = calculate_cog(components)

                if (cog > (drone_length/2 + (30/100)*drone_length/2)):
                    print(f"The center of gravity is too far to the right. Try again. for drone weight={d_w}, tank_weight={t_w}, arm_length={a_l}, arm_weight={a_w}")
                else:
                    force = get_required_thrust(cog, arm, drone, tank)    
                    print(f"CoG={cog:.3f} for drone weight={d_w}, tank_weight={t_w}, arm_length={a_l}, arm_weight={a_w}")    
                    print(f"Required thrust force: {force:.3f}")
