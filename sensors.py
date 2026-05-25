

class Sensor:
    def __init__(self, name, critical_value, actual_value):
        self.name = name
        self.critical_value = critical_value
        self.actual_value = actual_value

    def test(self):
        if (self.actual_value >= self.critical_value):
            print(f'Critical value for {self.name}')
            return True
        else:
            print(f'Safe value for {self.name}')
            return False
    def update_reading(self, new_value):
        self.actual_value = new_value
        print("updated value of sensor")

    def simulate_physics(self, vehicle):

        self.actual_value = float(self.actual_value)


class BrakeSensor(Sensor):
    def __init__(self, name, critical_value=50, actual_value=0):
        super().__init__(name, critical_value, actual_value)

    def simulate_physics(self, vehicle):
        speed_factor = vehicle.now_v / max(1, vehicle.max_v)
        wagon_factor = getattr(vehicle, "vagon_number", 0) * 0.8

        if vehicle.is_slowing:
            rise = 8.0 + (speed_factor * 12.0) + wagon_factor
            self.actual_value = min(100.0, round(self.actual_value + rise, 1))
        else:
            fall = 3.0 + (1.0 - speed_factor) * 4.0
            self.actual_value = max(0.0, round(self.actual_value - fall, 1))


class EngineSensor(Sensor):
    def __init__(self, name, critical_value=50, actual_value=30):
        super().__init__(name, critical_value, actual_value)

    def simulate_physics(self, vehicle):
        speed_factor = vehicle.now_v / max(1, vehicle.max_v)
        wagon_factor = getattr(vehicle, "vagon_number", 0) * 0.5

        if vehicle.is_slowing:
            cool_down = 2.5 + (1.0 - speed_factor) * 8.0
            self.actual_value = max(0.0, round(
                self.actual_value - cool_down, 1))
        elif vehicle.is_accelerating:
            base_heat = 1.5 + (speed_factor * 4.5) + wagon_factor
            if vehicle.now_v == 0:
                base_heat = 0
            self.actual_value = min(180.0, round(
                self.actual_value + base_heat, 1))
        elif not vehicle.is_accelerating and not vehicle.is_slowing:
            if vehicle.now_v != 0:
                
                base_heat = -4.2 + (speed_factor * 2.5) + wagon_factor
            if vehicle.now_v == 0:
                base_heat = 0
            self.actual_value = max(min(180.0, round(
                self.actual_value + base_heat, 1)),max(60+vehicle.now_v*0.1,vehicle.now_v-20))
