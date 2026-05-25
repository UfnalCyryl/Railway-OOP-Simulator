class Route:
    def __init__(self, distance=10, position=0, time=30):
        self.distance = distance
        self.position = position
        self.time = time
        self.total_time = 0
        self.station=False

    def progress(self, vehicle, delta_time):
        vehicle.update_position(delta_time)
        vehicle.update_sensors()
        self.total_time += delta_time

        traveled = vehicle.now_v * (delta_time / 3600)
        self.position = min(self.distance, self.position + traveled)
        if self.position==self.distance:
            self.station=True
            