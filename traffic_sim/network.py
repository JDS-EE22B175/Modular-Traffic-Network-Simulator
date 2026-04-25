class Road:
    def __init__(self, r_id, start_node, end_node, length, capacity):
        self.id = r_id
        self.start_node = start_node
        self.end_node = end_node
        self.length = length
        self.capacity = capacity
        
        self.traveling_vehicles = []
        self.waiting_queue = []
        
    def get_total_vehicles(self):
        return len(self.traveling_vehicles) + len(self.waiting_queue)

    def tick(self, tracker):
        # flag if the road is jammed
        if self.get_total_vehicles() >= self.capacity:
            tracker.record_capacity_tick(self.id)
            
        still_traveling = []
        for v in self.traveling_vehicles:
            v.driving_time += 1
            v.distance_traveled += v.speed
            
            # reached the junction, join the queue
            if v.distance_traveled >= self.length:
                v.distance_traveled = self.length
                v.state = "queued"
                self.waiting_queue.append(v)
            else:
                still_traveling.append(v)
        
        self.traveling_vehicles = still_traveling
        
        # bump waiting times
        for v in self.waiting_queue:
            v.waiting_time += 1
            
        tracker.record_queue(self.id, len(self.waiting_queue))


class Junction:
    def __init__(self, n_id):
        self.id = n_id
        self.in_roads = []
        self.out_roads = []
        self.rr_idx = 0 # round robin index to be fair to all incoming roads

    def tick(self, roads_dict):
        if not self.in_roads: 
            return
        
        # loop through incoming roads to find a car to move
        for _ in range(len(self.in_roads)):
            in_road_id = self.in_roads[self.rr_idx]
            in_road = roads_dict[in_road_id]
            
            # move to next road for the next tick
            self.rr_idx = (self.rr_idx + 1) % len(self.in_roads)

            if len(in_road.waiting_queue) > 0:
                v = in_road.waiting_queue[0]
                
                try:
                    current_node_idx = v.path.index(self.id)
                except ValueError:
                    continue # just a failsafe
                
                if current_node_idx + 1 < len(v.path):
                    next_node = v.path[current_node_idx + 1]
                    out_road_id = f"{self.id}->{next_node}"
                    out_road = roads_dict.get(out_road_id)

                    # if there is space on the next road, move the car
                    if out_road and out_road.get_total_vehicles() < out_road.capacity:
                        in_road.waiting_queue.pop(0)
                        v.distance_traveled = 0.0
                        v.state = "traveling"
                        out_road.traveling_vehicles.append(v)
                        break