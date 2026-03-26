class Device: 
    def __init__(self, id: int, name: str, device_type: str):
        self.id = id
        self.name = name
        self.device_type = device_type
        #self.user: User | None = None
        #self.measurements: list["Measurement"] = []