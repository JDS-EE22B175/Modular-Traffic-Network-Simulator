import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Visualizer:
    def __init__(self, engine, steps=100):
        self.engine = engine
        self.steps = steps
        # Map destinations to colors for the requirement
        self.dest_colors = {}
        self.color_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

    def get_color(self, dest_id):
        if dest_id not in self.dest_colors:
            idx = len(self.dest_colors) % len(self.color_palette)
            self.dest_colors[dest_id] = self.color_palette[idx]
        return self.dest_colors[dest_id]

    def animate(self, filename="traffic_sim.gif"):
        fig, ax = plt.subplots(figsize=(10, 7))
        pos = nx.get_node_attributes(self.engine.graph, 'pos')
        
        if not pos:
            pos = nx.kamada_kawai_layout(self.engine.graph)

        nx.draw_networkx_nodes(self.engine.graph, pos, ax=ax, node_color='#ecf0f1', node_size=700)
        nx.draw_networkx_edges(self.engine.graph, pos, ax=ax, arrowstyle='->', arrowsize=20, edge_color='#7f8c8d', width=1.5)
        nx.draw_networkx_labels(self.engine.graph, pos, ax=ax, font_size=10, font_weight="bold")
        
        ax.axis('off')
        self.drawn_vehicles = []

        def update(frame):
            for marker in self.drawn_vehicles:
                marker.remove()
            self.drawn_vehicles.clear()
            
            self.engine.tick()

            for road in self.engine.roads.values():
                x1, y1 = pos[road.start_node]
                x2, y2 = pos[road.end_node]
                
                # Plot moving (Circles)
                for v in road.traveling_vehicles:
                    frac = max(0.08, min(0.92, v.distance_traveled / road.length))
                    vx, vy = x1 + frac*(x2-x1), y1 + frac*(y2-y1)
                    
                    # Color is based on v.dest
                    scat = ax.scatter(vx, vy, color=self.get_color(v.dest), s=100, edgecolors='black', zorder=5)
                    self.drawn_vehicles.append(scat)

                # Plot queued (Squares)
                for i, v in enumerate(road.waiting_queue):
                    offset = max(0.1, 0.90 - (i * 0.05))
                    qx, qy = x1 + offset*(x2-x1), y1 + offset*(y2-y1)
                    
                    # Color is based on v.dest, marker is square
                    scat = ax.scatter(qx, qy, color=self.get_color(v.dest), s=100, edgecolors='black', marker='s', zorder=5)
                    self.drawn_vehicles.append(scat)

            ax.set_title(f"EE5150 Traffic Simulation | Tick: {self.engine.current_tick}")

        print(f"Generating animation ({self.steps} frames)...")
        ani = animation.FuncAnimation(fig, update, frames=self.steps, interval=150, repeat=False)
        ani.save(filename, writer='pillow', fps=8)
        print(f"Saved to {filename}")