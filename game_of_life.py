import numpy as np
import plotly.express as px
import pandas as pd

standard_rule = "B3S23"  # for Birth = 3 neighbors and Stays alive : 2 or 3

array3 = np.array(pd.read_excel("Array_3.xlsx", header=None).iloc[:20, :20])

N = 100
array_test = np.random.randint(2, size=(N*N)).reshape(N, N)
array1 = np.random.choice([0, 1], N*N, p=[0.1, 0.9]).reshape(N, N)
array2 = np.random.choice([0, 1], N*N, p=[0.92, 0.08]).reshape(N, N)

def neigboors_alive(grid):
    # for an array return an array of the nb of living neighbors
    count_array = np.zeros(shape=grid.shape)
    for (i, j), value in np.ndenumerate(grid):
        array_1 = [(i-1), i, (i+1)]
        array_2 = [(j - 1), j, (j + 1)]
        mesh = np.array(np.meshgrid(array_1, array_2)).T.reshape(-1, 2)
        # remove negative values, remove values superior to the grid shape
        mesh = [(k[0], k[1]) for k in mesh if 0 <= k[0] < grid.shape[0] and 0 <= k[1] < grid.shape[1]]
        # sum and remove value for the central cell

        count_array[i, j] = int(sum([grid[c] for c in mesh]) - grid[i, j])
    return count_array


def update_grid(neighbors, dead_to_alive, staying_alive):
    # make dict of what should be alive or be reborn based on rules
    # 1 for alive, 0 for dead
    living_rules = {u: 1 if u in staying_alive+dead_to_alive else 0 for u in np.unique(neighbors)}
    # apply on the count of neighbors
    living = np.vectorize(lambda x: living_rules[x])
    # update grid
    return living(neighbors)


class Gol:

    def __init__(self, initial_state, rules, duration=10):
        assert isinstance(duration, int) and duration > 1, "duration must be an integer superior to one"
        assert isinstance(initial_state, np.ndarray), "format of the initial board should be a np array"
        self.initial_state = initial_state
        self.long = self.initial_state.shape[0]
        self.width = self.initial_state.shape[1]
        self.duration = duration
        self.rules = rules
        self.dead_to_alive, self.staying_alive = self.parsing_rules()

    def parsing_rules(self):
        return [int(i) for i in self.rules.split("B")[1].split("S")[0]], [int(i) for i in self.rules.split("S")[1]]

    def run_game(self):
        life_journey = np.zeros(shape=(self.duration, self.long, self.width))
        for t in range(0, self.duration):
            if t == 0:
                life_journey[t, :, :] = self.initial_state
                #neighbor_grid = neigboors_alive(grid=self.initial_state)
                neighbor_grid = neigboors_alive(grid=self.initial_state)
            else:
                neighbor_grid = neigboors_alive(grid=life_journey[t-1])
                life_journey[t, :, :] = update_grid(neighbors=neighbor_grid,
                                                dead_to_alive=self.dead_to_alive, staying_alive=self.staying_alive)
        # replace to take into account RBG rules : 255 is white: white is dead so 0 for us
        life_journey[life_journey == 0] = 255
        life_journey[life_journey == 1] = 0
        return life_journey


if __name__ == "__main__":
    A = Gol(initial_state=array2, rules=standard_rule, duration=50).run_game()
    fig = px.imshow(A, animation_frame=0, binary_string=True,
                     labels=dict(animation_frame="time steps in the life journey"))
    fig.show()
