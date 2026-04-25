import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import traceback

class Visualizer:
    def __init__(self, engine, steps=100):
        self.engine = engine
        self.steps = steps

    def animate(self, filename="traffic_simulation.gif"):
        fig, ax = plt.subplots(figsize=(10, 7))
        pos = nx.get_node_attributes(self.engine.graph, 'pos')
        
        # fallback layout
        if not pos or len(pos) != len(self.engine.graph.nodes):
            print("Missing pos data, using auto layout...")
            pos = nx.kamada_kawai_layout(self.engine.graph)

        # --- DRAW THE STATIC NETWORK ONLY ONCE ---
        nx.draw_networkx_nodes(self.engine.graph, pos, ax=ax, node_color='lightgrey', node_size=600)
        nx.draw_networkx_edges(self.engine.graph, pos, ax=ax, arrowstyle='->', arrowsize=20, edge_color='black', width=1.5)
        nx.draw_networkx_labels(self.engine.graph, pos, ax=ax, font_size=10, font_weight="bold")
        
        ax.axis('off')
        
        # Track our dynamic car markers
        self.drawn_vehicles = []

        def update(frame):
            # Erase only the cars from the previous frame
            for marker in self.drawn_vehicles:
                marker.remove()
            self.drawn_vehicles.clear()
            
            # Advance the simulation logic
            self.engine.tick()

            # Draw the new car positions
            for road in self.engine.roads.values():
                if road.start_node not in pos or road.end_node not in pos:
                    continue
                    
                x1, y1 = pos[road.start_node]
                x2, y2 = pos[road.end_node]
                
                # moving cars (lime)
                for v in road.traveling_vehicles:
                    fraction = v.distance_traveled / road.length
                    fraction = max(0.08, min(0.92, fraction)) 
                    vx = x1 + fraction * (x2 - x1)
                    vy = y1 + fraction * (y2 - y1)
                    
                    scat = ax.scatter(vx, vy, color='lime', s=80, edgecolors='black', zorder=5)
                    self.drawn_vehicles.append(scat) # Save the marker so we can erase it next tick

                # queued cars (red squares)
                for i, v in enumerate(road.waiting_queue):
                    offset = 0.90 - (i * 0.04) 
                    offset = max(0.1, offset) 
                    qx = x1 + offset * (x2 - x1)
                    qy = y1 + offset * (y2 - y1)
                    
                    scat = ax.scatter(qx, qy, color='red', s=80, edgecolors='darkred', marker='s', zorder=5)
                    self.drawn_vehicles.append(scat) # Save the marker so we can erase it next tick

            ax.set_title(f"Traffic Sim | Tick: {self.engine.current_tick} | Cars on road: {len(self.engine.active_vehicles)}")

        # Restored the original print statement you requested
        print(f"Generating animation ({self.steps} frames)...")
        ani = animation.FuncAnimation(fig, update, frames=self.steps, interval=150, repeat=False)
        
        try:
            ani.save(filename, writer='pillow', fps=8)
            print(f"Saved to {filename}!")
        except Exception as e:
            print(f"Couldn't save gif: {e}")
            traceback.print_exc()