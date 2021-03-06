from matplotlib.animation import FuncAnimation
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

from driving_sim.driving_gui.patch_utils import *
from driving_sim.driving_utils.constants import *

class GUI:
    '''
    Controls the simulator graphics
    '''
    def __init__(self, sim_state):
        self.state = sim_state
        self.fig = plt.figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, self.state.x_bound)
        self.ax.set_ylim(0, self.state.y_bound)
        self.pixel_width, self.pixel_height = self.fig.get_size_inches() * self.fig.dpi
        self.scale = 1., 1.

    def run_sim(self, start_t=0, real_t=0.1):
        '''
        Runs the simulator from the starting timestep until the end
        start_t: The time to start the simulator from
        real_t: How long the simulator pauses between timesteps
        '''
        start_timestep = int(start_t)
        end_timestep = int(self.state.horizon)
        interval = int(1000 * real_t)
        frames = range(start_timestep, end_timestep+1)

        animation = FuncAnimation(self.fig, self.draw_frame, frames=frames, interval=interval)
        plt.show()

    def add_timestep(self, time):
        '''
        Draws the simulator's state at a given timestep
        '''
        self.clear()
        self.add_objects(time)
        self.add_surfaces(time)

    def draw_timestep(self, time):
        '''
        Renders the simulator's state at a given timestep
        '''
        self.clear()
        self.add_objects(time)
        self.add_surfaces(time)
        plt.show()

    def draw_frame(self, time):
        '''
        Draws the current timestep if in range, otherwise closes the plot
        '''
        if time >= 0 and time < self.state.horizon:
            self.add_timestep(time)
        else:
            plt.close()

    def add_collection(self, to_render, time, zorder=0):
        '''
        Add all patches for a given set of objects or surfaces
        '''
        patches = []
        for r in to_render:
            for p in r.get_patches(self.scale, time):
                p.zorder = zorder
                self.ax.add_artist(p)

    def add_vehicles(self, time):
        '''
        Add all vehicles to be rendered at a given timestep
        '''
        vehicles = self.state.external_vehicles
        self.add_collection(vehicles, time, 5)

        vehicles = self.state.user_vehicles
        self.add_collection(vehicles, time, 6)

    def add_crates(self, time):
        '''
        Add all crates to be rendered at a given timestep
        '''
        crates = self.state.crates
        self.add_collection(crates, time, 4)

    def add_obstacles(self, time):
        '''
        Add all obstacles to be rendered at a given timestep
        '''
        obstacles = self.state.obstacles
        self.add_collection(obstacles, time, 3)

    def add_roads(self, time):
        '''
        Add all roads to be rendered at a given timestep
        '''
        roads = self.state.roads.values()
        self.add_collection(roads, time, 1)

    def add_lots(self, time):
        '''
        Add all lots to be rendered at a given timestep
        '''
        lots = self.state.lots.values()
        self.add_collection(lots, time, 2)

    def add_objects(self, time):
        '''
        Add all objects to be rendered at a given timestep
        '''
        self.add_vehicles(time)
        self.add_crates(time)
        self.add_obstacles(time)

    def add_surfaces(self, time):
        '''
        Add all surfaces to be rendered
        '''
        self.add_roads(time)
        self.add_lots(time)

    def clear(self):
        '''
        Clears the previously rendered drawing
        '''
        self.ax.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, self.state.x_bound)
        self.ax.set_ylim(0, self.state.y_bound)
