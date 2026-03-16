class Device: 
    def init(self, id: int, name: str, type: str):
        self.id = id
        self.name = name
        self.type = type
        self.user: User | None = None
        self.measurements: list["Measurement"] = []