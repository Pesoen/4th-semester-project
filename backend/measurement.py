from datetime import datetime


class Measurement:
    def __init__(self, measurement_id: int, device_id: int, value: float, time: datetime):
        self.measurement_id = measurement_id
        self.device_id = device_id
        self.value = value
        self.time = time