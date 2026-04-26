class Tracker:
    def __init__(self):
        self.spawned = 0
        self.exited = 0
        self.total_ticks = 0
        
        self.travel_times = []
        self.driving_times = []
        self.waiting_times = []
        
        # New: Destination-specific tracking
        self.dest_stats = {} # {dest_id: [travel_times]}
        
        self.max_queue_lengths = {}
        self.capacity_ticks = {}

    def record_spawn(self):
        self.spawned += 1

    def record_exit(self, total_time, driving_time, waiting_time, dest_id):
        self.exited += 1
        self.travel_times.append(total_time)
        self.driving_times.append(driving_time)
        self.waiting_times.append(waiting_time)
        
        if dest_id not in self.dest_stats:
            self.dest_stats[dest_id] = []
        self.dest_stats[dest_id].append(total_time)

    def record_queue(self, road_id, q_len):
        if road_id not in self.max_queue_lengths:
            self.max_queue_lengths[road_id] = 0
        self.max_queue_lengths[road_id] = max(self.max_queue_lengths[road_id], q_len)
        
    def record_capacity_tick(self, road_id):
        if road_id not in self.capacity_ticks:
            self.capacity_ticks[road_id] = 0
        self.capacity_ticks[road_id] += 1

    def print_summary(self):
        print("\n" + "="*45)
        print("EE5150 FINAL SIMULATION REPORT")
        print("="*45)
        print(f"Total Duration: {self.total_ticks} ticks")
        print(f"Cars Spawned:   {self.spawned}")  # Added
        print(f"Cars Exited:    {self.exited}")   # Added
        print(f"Throughput:     {self.exited / self.total_ticks:.2f} cars/tick")
        
        if self.exited > 0:
            print(f"\nGlobal Average Times:")
            print(f"  Total Travel: {sum(self.travel_times)/self.exited:.1f} ticks")
            print(f"  Wait Delay:   {sum(self.waiting_times)/self.exited:.1f} ticks")

            print(f"\nStats by Destination:")
            for dest, times in self.dest_stats.items():
                avg = sum(times)/len(times)
                print(f"  To {dest:<5}: {len(times):>3} cars reached, Avg Time: {avg:.1f}")
            
        print(f"\n{'Road ID':<12} | {'Max Queue':<10} | {'% Saturation'}")
        print("-" * 45)
        for r in sorted(self.max_queue_lengths.keys()):
            max_q = self.max_queue_lengths[r]
            util = (self.capacity_ticks.get(r, 0) / self.total_ticks) * 100
            print(f"{r:<12} | {max_q:<10} | {util:.1f}%")
        print("="*45 + "\n")