from traffic_sim.engine import Engine
from traffic_sim.visualizer import Visualizer

def main():
    engine = Engine()

    # set up the grid
    engine.add_node("Src1", "source", rate=0.6, pos=(0, 4))
    engine.add_node("Src2", "source", rate=0.4, pos=(0, 0))
    
    engine.add_node("J1", "junction", pos=(3, 4))
    engine.add_node("J2", "junction", pos=(3, 0))
    engine.add_node("J3", "junction", pos=(6, 2))
    
    engine.add_node("Snk1", "sink", pos=(9, 4))
    engine.add_node("Snk2", "sink", pos=(9, 0))

    # connect the roads
    engine.add_road("Src1", "J1", length=100, capacity=10)
    engine.add_road("Src2", "J2", length=100, capacity=10)
    
    engine.add_road("J1", "J2", length=150, capacity=15)
    engine.add_road("J2", "J1", length=150, capacity=15)
    
    engine.add_road("J1", "J3", length=80,  capacity=8)
    engine.add_road("J2", "J3", length=120, capacity=12)
    
    engine.add_road("J3", "Snk1", length=60, capacity=6)
    engine.add_road("J3", "Snk2", length=60, capacity=6)

    # run it
    viz = Visualizer(engine, steps=200)
    viz.animate("traffic_sim.gif")
    
    engine.tracker.print_summary()

if __name__ == "__main__":
    main()