class Vehicle:
    def __init__(self, v_id, source_id, dest_id, path, start_time, speed):
        self.id = v_id
        self.source = source_id
        self.dest = dest_id
        self.path = path
        self.start_time = start_time
        self.speed = speed
        
        # tracking where the car is physically
        self.distance_traveled = 0.0
        self.state = "traveling" # either traveling or queued
        
        # for stats later
        self.driving_time = 0
        self.waiting_time = 0