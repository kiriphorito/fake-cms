import random as rnd
import numpy as np

EMPTY = 0
MARINE = 1
MINERAL = 2

ACTION_MOVE_UP = 'moveup'
ACTION_MOVE_DOWN = 'movedown'
ACTION_MOVE_LEFT = 'moveleft'
ACTION_MOVE_RIGHT = 'moveright'

action_space = [
    ACTION_MOVE_UP,
    ACTION_MOVE_DOWN,
    ACTION_MOVE_LEFT,
    ACTION_MOVE_RIGHT,
]

class Fcms:
    def __init__(self, marines = 1, shards = 20, grid_x = 5, grid_y = 5, verbose = False):
        self.verbose = verbose

        self.absolute_shards = None
        self.absolute_number_of_shards = shards

        self.number_of_marines = marines
        self.number_of_shards = shards
        self.grid_width = grid_x
        self.grid_height = grid_y
        self.grid_observation = None
        self.position_shards = None
        self.position_marines = None
        self.reset()
        self.reward = 0
        self.action_space = action_space

    def reset(self):
        self.position_shards = []
        self.collected_shards = []
        self.position_marines = []
        self.absolute_shards = []

        self.number_of_shards = self.absolute_number_of_shards

        while len(self.position_shards) < self.number_of_shards:
            random_location = [rnd.randint(0,self.grid_width - 1), rnd.randint(0,self.grid_height - 1)]
            if random_location not in self.position_shards:
                self.position_shards.append(random_location)
                self.absolute_shards.append(random_location)
        while len(self.position_marines) < self.number_of_marines:
            random_location = [rnd.randint(0,self.grid_width - 1), rnd.randint(0,self.grid_height - 1)]
            if random_location not in self.position_shards and random_location not in self.position_marines:
                self.position_marines.append(random_location)
        if self.verbose:
            print("Marines: ", self.position_marines)
            print("Shards: ", self.position_shards)
   

    def observation(self):
        self.grid_observation = [[0 for i in range(self.grid_width)] for j in range(self.grid_height)]
        for shard in self.position_shards:
            self.grid_observation[shard[0]][shard[1]] = MINERAL
        for marine in self.position_marines:
            self.grid_observation[marine[0]][marine[1]] = MARINE
        if self.verbose:
            print("-------------")
            print(self.position_marines)
            for x in range(0, self.grid_height):
                print("",end = " ")
                for y in range(0, self.grid_width):
                    print(self.grid_observation[y][x], end = " ")
                print()
        return self.grid_observation

    def observation_keras(self):
        observation = []
        marine_x = []
        marine_y = []
        shard_x = []
        shard_y = []

        # for x in range(self.number_of_marines):
        #     marine_x.append(self.position_marines[x][0])
        #     marine_x.append(self.position_marines[x][1])
        # for x in range(self.number_of_shards):
        #     shard_x.append(self.position_shards[x][0])
        #     shard_x.append(self.position_shards[x][1])
        # observation = [np.array(marine_x), np.array(marine_y), np.array(shard_x), np.array(shard_y)]

        for x in range(self.number_of_marines):
            for y in range(0, 2):
                observation.append(self.position_marines[x][y])
        for x in range(self.absolute_number_of_shards):
            for y in range(0, 2):
                # print(self.absolute_shards)
                # print("i: ", x)
                # print("j: ", y)
                observation.append(self.absolute_shards[x][y])
            if self.absolute_shards[x] in self.position_shards:
                observation.append(1)
            else:
                observation.append(0)

        return observation


    def collision_check(self, position):
        if position in self.position_shards:
            self.position_shards.remove(position)
            self.number_of_shards -= 1
            self.reward += 1

    def boundary_check(self, marine):
        if self.position_marines[marine][0] >= self.grid_width:
            self.position_marines[marine][0] = self.grid_width - 1
        elif self.position_marines[marine][0] < 0:
            self.position_marines[marine][0] = 0
        if self.position_marines[marine][1] >= self.grid_height:
            self.position_marines[marine][1] = self.grid_height - 1
        elif self.position_marines[marine][1] < 0:
            self.position_marines[marine][1] = 0

    def action(self, action, marine = 0):
        action = action_space[action]
        if action == ACTION_MOVE_UP:
            self.action_up(marine)
        elif action == ACTION_MOVE_DOWN:
            self.action_down(marine)
        elif action == ACTION_MOVE_LEFT:
            self.action_left(marine)
        elif action == ACTION_MOVE_RIGHT:
            self.action_right(marine)

    def action_up(self, marine = 0):
        new_position = self.position_marines[marine]
        new_position[1] -= 1
        self.position_marines[marine] = new_position
        self.boundary_check(marine)
        self.collision_check(new_position)

    def action_down(self, marine = 0):
        new_position = self.position_marines[marine]
        new_position[1] += 1
        self.position_marines[marine] = new_position
        self.boundary_check(marine)
        self.collision_check(new_position)

    def action_left(self, marine = 0):
        new_position = self.position_marines[marine]
        new_position[0] -= 1
        self.position_marines[marine] = new_position
        self.boundary_check(marine)
        self.collision_check(new_position)

    def action_right(self,marine = 0):
        new_position = self.position_marines[marine]
        new_position[0] += 1
        self.position_marines[marine] = new_position
        self.boundary_check(marine)
        self.collision_check(new_position)

    # OpenAI gym conform
    def step(self, action, marine = 0):
        self.reward = 0
        self.action(action, marine)

        done = False
        if len(self.position_shards) == 0:
            done = True

        reward = self.reward

        return None , reward, done, {}


# fcms = Fcms(2, 20, 8, 8, True)
# print(fcms.observation_keras())

# fcms.action_up()
# fcms.observation()
# fcms.action_down()
# fcms.observation()
# fcms.action_left()
# fcms.observation()
# fcms.action_up()
# fcms.observation()
# fcms.action_up()
# fcms.observation()
# fcms.action_right()
# fcms.observation()
