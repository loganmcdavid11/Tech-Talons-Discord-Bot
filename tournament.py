# Tournament Class 
class Tournament:
    # Constructor
    def __init__(self, name, start_date, end_date, location, aof_time, field_address, lodging_address):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.aof_time = aof_time
        self.field_address = field_address
        self.lodging_address = lodging_address
        
    # Output
    def __repr__(self):
        return (f"{self.name}\n"
                f"Date: {self.start_date} to {self.end_date}\n"
                f"Location: {self.location}\n"
                f"AOF Time: {self.aof_time}\n"
                f"Field Address: {self.field_address}\n"
                f"Lodging Address: {self.lodging_address}")