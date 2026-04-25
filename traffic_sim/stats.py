class Tracker:
    def __init__(self):
        self.spawned = 0
        self.exited = 0
        self.total_ticks = 0
        
        self.travel_times = []
        self.driving_times = []
        self.waiting_times = []
        
        self.max_queue_lengths = {}
        self.capacity_ticks = {}

    def record_spawn(self):
        self.spawned += 1

    def record_exit(self, total_time, driving_time, waiting_time):
        self.exited += 1
        self.travel_times.append(total_time)
        self.driving_times.append(driving_time)
        self.waiting_times.append(waiting_time)

    def record_queue(self, road_id, q_len):
        if road_id not in self.max_queue_lengths:
            self.max_queue_lengths[road_id] = 0
        self.max_queue_lengths[road_id] = max(self.max_queue_lengths[road_id], q_len)
        
    def record_capacity_tick(self, road_id):
        if road_id not in self.capacity_ticks:
            self.capacity_ticks[road_id] = 0
        self.capacity_ticks[road_id] += 1

    def print_summary(self):
        print("\n--- Final Simulation Results ---")
        print(f"Ticks ran: {self.total_ticks}")
        print(f"Cars spawned: {self.spawned}")
        print(f"Cars arrived: {self.exited}")
        
        if self.total_ticks > 0:
            throughput = self.exited / self.total_ticks
            print(f"Throughput: {throughput:.2f} cars/tick")
        
        if self.exited > 0:
            avg_time = sum(self.travel_times) / self.exited
            avg_drive = sum(self.driving_times) / self.exited
            avg_wait = sum(self.waiting_times) / self.exited
            print(f"\nAvg trip time: {avg_time:.1f} ticks")
            print(f"  -> Driving: {avg_drive:.1f} ticks")
            print(f"  -> Waiting: {avg_wait:.1f} ticks")
            
        print("\nRoad Stats (ID | Max Queue | % Jammed):")
        for r in sorted(self.max_queue_lengths.keys()):
            max_q = self.max_queue_lengths[r]
            cap_ticks = self.capacity_ticks.get(r, 0)
            utilization = (cap_ticks / self.total_ticks) * 100 if self.total_ticks > 0 else 0
            print(f"{r:<12} | {max_q:<9} | {utilization:.1f}%")
        print("--------------------------------\n")