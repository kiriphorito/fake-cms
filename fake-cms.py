import random as rnd

EMPTY = 0
MARINE = 1
MINERAL = 2

class Fcms:
    def __init__(self, marines = 1, shards = 20, grid_x = 5, grid_y = 5):
        self.number_of_marines = marines
        self.number_of_shards = shards
        self.grid_width = grid_x
        self.grid_height = grid_y
        self.grid_observation = None
        self.position_shards = None
        self.position_marines = None
        self.reset()

    def reset(self):
        self.position_shards = []
        self.position_marines = []
        while len(self.position_shards) < self.number_of_shards:
            random_location = [rnd.randint(0,self.grid_width - 1), rnd.randint(0,self.grid_height - 1)]
            if random_location not in self.position_shards:
                self.position_shards.append(random_location)
        while len(self.position_marines) < self.number_of_marines:
            random_location = [rnd.randint(0,self.grid_width - 1), rnd.randint(0,self.grid_height - 1)]
            if random_location not in self.position_shards and random_location not in self.position_marines:
                self.position_marines.append(random_location)
        print(self.position_shards)
        print(self.position_marines)

    def observation(self):
        self.grid_observation = [[0 for i in range(self.grid_width)] for j in range(self.grid_height)]
        for shard in self.position_shards:
            self.grid_observation[shard[0]][shard[1]] = MINERAL
        for marine in self.position_marines:
            self.grid_observation[marine[0]][marine[1]] = MARINE
        print(self.position_marines)
        for x in range(0, self.grid_height):
            print("",end = " ")
            for y in range(0, self.grid_width):
                print(self.grid_observation[y][x], end = " ")
            print()
        return self.grid_observation

    def collision_check(self, position):
        if position in self.position_shards:
            self.position_shards.remove(position)

    def boundary_check(self, marine):
        if self.position_marines[marine][0] >= self.grid_width:
            self.position_marines[marine][0] = self.grid_width - 1
        elif self.position_marines[marine][0] < 0:
            self.position_marines[marine][0] = 0
        if self.position_marines[marine][1] >= self.grid_height:
            self.position_marines[marine][1] = self.grid_height - 1
        elif self.position_marines[marine][1] < 0:
            self.position_marines[marine][1] = 0

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

fcms = Fcms()
print(fcms.number_of_shards)
print(fcms.number_of_marines)
fcms.observation()

print("-------------")
fcms.action_up()
fcms.observation()
print("-------------")
fcms.action_down()
fcms.observation()
print("-------------")
fcms.action_left()
fcms.observation()
print("-------------")
fcms.action_up()
fcms.observation()
print("-------------")
fcms.action_up()
fcms.observation()
print("-------------")
fcms.action_right()
fcms.observation()
