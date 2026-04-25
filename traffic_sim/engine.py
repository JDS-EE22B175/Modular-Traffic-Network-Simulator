import random
import networkx as nx
from .network import Road, Junction
from .vehicle import Vehicle
from .stats import Tracker

class Engine:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.roads = {}
        self.junctions = {}
        self.sources = {}
        self.sinks = []
        
        self.tracker = Tracker()
        self.current_tick = 0
        self.vehicle_counter = 0
        self.active_vehicles = []

    def add_node(self, n_id, node_type, rate=0.0, pos=(0,0)):
        self.graph.add_node(n_id, type=node_type, pos=pos)
        if node_type == "junction":
            self.junctions[n_id] = Junction(n_id)
        elif node_type == "source":
            self.sources[n_id] = rate
        elif node_type == "sink":
            self.sinks.append(n_id)

    def add_road(self, start_node, end_node, length=100, capacity=10):
        r_id = f"{start_node}->{end_node}"
        road = Road(r_id, start_node, end_node, length, capacity)
        self.roads[r_id] = road
        self.graph.add_edge(start_node, end_node, road_ref=road, weight=length)
        
        if start_node in self.junctions:
            self.junctions[start_node].out_roads.append(r_id)
        if end_node in self.junctions:
            self.junctions[end_node].in_roads.append(r_id)

    def get_route(self, source, dest):
        try:
            return nx.shortest_path(self.graph, source=source, target=dest, weight='weight')
        except nx.NetworkXNoPath:
            return None

    def tick(self):
        self.current_tick += 1
        self.tracker.total_ticks = self.current_tick

        # clear sinks first to free up space
        for sink_id in self.sinks:
            in_edges = [f"{u}->{sink_id}" for u, v in self.graph.in_edges(sink_id)]
            for r_id in in_edges:
                road = self.roads[r_id]
                if len(road.waiting_queue) > 0:
                    v = road.waiting_queue.pop(0)
                    self.active_vehicles.remove(v)
                    total_time = self.current_tick - v.start_time
                    self.tracker.record_exit(total_time, v.driving_time, v.waiting_time)

        # process intersections
        for j in self.junctions.values():
            j.tick(self.roads)

        # update cars on the roads
        for r in self.roads.values():
            r.tick(self.tracker)

        # spawn new cars using standard probability
        for src_id, rate in self.sources.items():
            if random.random() < rate:
                out_edges = [f"{src_id}->{v}" for u, v in self.graph.out_edges(src_id)]
                if not out_edges: 
                    continue
                
                start_road = self.roads[out_edges[0]]
                
                # only spawn if there's room on the entry road
                if start_road.total_vehicles() < start_road.capacity:
                    dest_id = random.choice(self.sinks)
                    path = self.get_route(src_id, dest_id)
                    
                    if path:
                        self.vehicle_counter += 1
                        # TODO: maybe make speed depend on road later?
                        speed = random.uniform(5.0, 10.0) 
                        v = Vehicle(self.vehicle_counter, src_id, dest_id, path, self.current_tick, speed)
                        
                        self.active_vehicles.append(v)
                        start_road.traveling_vehicles.append(v)
                        self.tracker.record_spawn()