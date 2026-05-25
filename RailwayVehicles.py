from sensors import  BrakeSensor, EngineSensor


class RailwayVehicle:
    def __init__(self, id, max_v, now_v, door_open, capacity):
        self.id = id
        self.max_v = max_v
        self.now_v = now_v
        self.door_open = door_open
        self.capacity = capacity
        self.sensors = [
            EngineSensor(name='Engine_Temperature',
                         critical_value=105.0, actual_value=70.0),
            BrakeSensor(name='Brake_Sensor',
                        critical_value=50.0, actual_value=40.0)
        ]
        self.is_slowing = False
        self.is_accelerating = False
        self.total_dystans = 0

    def safety_check(self):
        return self.now_v == 0

    def open_door(self):
        if self.safety_check() and not self.door_open:
            self.door_open = True
            print("Door opened")
        elif self.safety_check() and self.door_open:
            print("Door already open")
        elif not self.safety_check() and not self.door_open:
            print("It is not safe to open the door")

    def update_sensors(self):
        for sensor in self.sensors:
            sensor.simulate_physics(self)
        

    def brake(self):
        self.now_v = max(0, self.now_v - 10)
        print(f"Braking to {self.now_v}")
        self.is_slowing = True
        self.update_sensors()
        self.is_slowing = False

    def breaking(self):
        return self.brake()

    def system_check(self):
        failed_sensors = []
        for sensor in self.sensors:
            if sensor.test():
                failed_sensors.append(sensor.name)

        return failed_sensors

    def accelerate(self):
        if self.door_open:
            print("Cannot accelerate with open doors")
            return False
        self.is_accelerating=True
        self.now_v = min(self.max_v, self.now_v + 20)
        self.update_sensors()
        self.is_accelerating=False

        return True

    def update_position(self, delta_time):  # delta in secounds
        time_in_hours = delta_time / 3600
        if (self.now_v > 0):
            self.total_dystans += (self.now_v*time_in_hours)


class Tram(RailwayVehicle):
    def __init__(self, id, max_v, now_v, door_open, capacity):
        super().__init__(id, max_v, now_v, door_open, capacity)

    def ring_bell(self):
        print("Ring")

    def brake(self):
        self.now_v = max(0, self.now_v - 20)
        print(f"Braking to {self.now_v}")
        self.is_slowing = True
        self.update_sensors()
        self.is_slowing = False

    def breaking(self):
        return self.brake()


class Train(RailwayVehicle):
    def __init__(self, id, max_v, now_v, door_open, capacity, vagon_number, max_vagon_number):
        super().__init__(id, max_v, now_v, door_open, capacity)
        self.vagon_number = vagon_number
        self.max_vagon_number = max_vagon_number

    def connect_vagon(self, number):
        if (self.max_vagon_number >= self.vagon_number+number):
            self.vagon_number += number
        else:
            print(
                f'Max ammount of vagons {self.max_vagon_number} has been reached after adding {self.max_vagon_number - self.vagon_number}')
            self.vagon_number = self.max_vagon_number

    def disconnect_vagon(self, number):
        self.vagon_number = max(0, self.vagon_number-number)
