from traffic_sim.engine_poisson import Engine  # Change to .engine if you prefer the Bernoulli version
from traffic_sim.visualizer import Visualizer

def main():
    engine = Engine()

    # ==========================================
    # 1. DEFINE NODES (with visual grid positions)
    # ==========================================
    
    # Left-side Sources & Sinks (x = 0)
    engine.add_node("S1_S4", "source", rate=0.6, pos=(0, 4))
    engine.add_node("S2_S5", "source", rate=0.5, pos=(0, 2))
    engine.add_node("K3_K4", "sink", pos=(0, 0))
    
    # Right-side Sources & Sinks (x = 9)
    engine.add_node("K2",    "sink", pos=(9, 4))
    engine.add_node("S3",    "source", rate=0.4, pos=(9, 2))
    engine.add_node("K1_K5", "sink", pos=(9, 0))

    # Internal 2x3 Junction Grid (x = 3 and x = 6)
    engine.add_node("J_TL", "junction", pos=(3, 4))  # Top-Left
    engine.add_node("J_TR", "junction", pos=(6, 4))  # Top-Right
    engine.add_node("J_ML", "junction", pos=(3, 2))  # Mid-Left
    engine.add_node("J_MR", "junction", pos=(6, 2))  # Mid-Right
    engine.add_node("J_BL", "junction", pos=(3, 0))  # Bot-Left
    engine.add_node("J_BR", "junction", pos=(6, 0))  # Bot-Right


    # ==========================================
    # 2. DEFINE ROADS
    # ==========================================

    # A. External Connections (1-way to/from grid)
    engine.add_road("S1_S4", "J_TL", length=100, capacity=10)
    engine.add_road("S2_S5", "J_ML", length=100, capacity=10)
    engine.add_road("J_BL", "K3_K4", length=100, capacity=10)
    
    engine.add_road("J_TR", "K2", length=100, capacity=10)
    engine.add_road("S3", "J_MR", length=100, capacity=10)
    engine.add_road("J_BR", "K1_K5", length=100, capacity=10)

    # B. Internal Grid - Horizontal (Bi-directional)
    engine.add_road("J_TL", "J_TR", length=150, capacity=15)
    engine.add_road("J_TR", "J_TL", length=150, capacity=15)
    
    engine.add_road("J_ML", "J_MR", length=150, capacity=15)
    engine.add_road("J_MR", "J_ML", length=150, capacity=15)
    
    engine.add_road("J_BL", "J_BR", length=150, capacity=15)
    engine.add_road("J_BR", "J_BL", length=150, capacity=15)

    # C. Internal Grid - Vertical (Bi-directional)
    engine.add_road("J_TL", "J_ML", length=100, capacity=10)
    engine.add_road("J_ML", "J_TL", length=100, capacity=10)
    
    engine.add_road("J_ML", "J_BL", length=100, capacity=10)
    engine.add_road("J_BL", "J_ML", length=100, capacity=10)
    
    engine.add_road("J_TR", "J_MR", length=100, capacity=10)
    engine.add_road("J_MR", "J_TR", length=100, capacity=10)
    
    engine.add_road("J_MR", "J_BR", length=100, capacity=10)
    engine.add_road("J_BR", "J_MR", length=100, capacity=10)


    # ==========================================
    # 3. RUN SIMULATION & VISUALIZE
    # ==========================================
    
    # 250 frames should give a great view of traffic migrating across the grid
    viz = Visualizer(engine, steps=250)
    viz.animate("traffic_sim.gif")
    
    engine.tracker.print_summary()

if __name__ == "__main__":
    main()