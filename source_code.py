import random
import math
import heapq

# Parameters of the program is given below, please specify the values of the parameters before running the program
# according to the requirements of the case

width = 100 # horizontal length of the area in number of (1x1) unit squares 
height = 100 # vertical length of the area in number of (1x1) unit squares
sense_radius = 10 # sensing radius of sensors, same for all sensors, any whole number
max_num_of_sensors = 75 # maximum number of sensors to be placed in the area
min_sep_length = 1 # minimum seperation length between sensors, any multiplier with sensing radius
sensor_placed_ids = [] # ids of the unit squares where sensors are placed
covered_ids = set() # ids of the unit squares covered by sensors
rock_density = 0.2 # density of rocks in the area, black id number over whole grid area
max_number_of_black_ids = width*height*rock_density # maximum number of black ids to be placed in the area
max_rock_length = sense_radius # maximum length for an obstacle is bounded with sensing radius of sensors
rock_number = 10 # specifies the number of starting points for obstacles inside obstacle creation loop

# The code below is the implementation of the algorithm that places sensors in the area

# Function for getting the coordinate of a unit square with id
def get_coordinate(id):
    return id%width, id//width

# Function for getting the id of a unit square with coordinates
def get_id(x, y):
    return x + y*width

# Function for selecting a random integer between a and b uniformly
def uniform_select(a, b):
    x = random.uniform(a, b+1)
    if(x != b+1):
        return math.floor(x)
    else:
        return math.floor(random.uniform(a, b))

# Function for updating the coordinates of a unit square with a movement vector
def update_coordinates(x, y, movement):
    x += movement[0]
    y += movement[1]
    return x, y

# Function for getting the distance between two unit squares with ids
def get_distance(id1, id2):
    x1, y1 = get_coordinate(id1)
    x2, y2 = get_coordinate(id2)
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

# Function for calculating the slope between two unit squares with coordinates
def calculate_slope(x1, y1, x2, y2):
    if (x1 == x2 and y2 > y1):
        return math.inf
    elif (x1 == x2 and y2 < y1):
        return -math.inf
    return (y2-y1)/(x2-x1)

# Function for getting the relative slope interval between two unit squares with ids
def get_relative_slope_interval(id1, id2):
    x1, y1 = get_coordinate(id1)
    x2, y2 = get_coordinate(id2)
    if (x2 > x1 and y2 > y1):
        lower_slope = calculate_slope(x1,y1, x2+0.5, y2-0.5)
        higher_slope = calculate_slope(x1,y1, x2-0.5, y2+0.5)
        return [1, [get_distance(id1, id2), lower_slope, higher_slope]]
    elif (x2 < x1 and y2 > y1):
        lower_slope = calculate_slope(x1,y1, x2+0.5, y2+0.5)
        higher_slope = calculate_slope(x1,y1, x2-0.5, y2-0.5)
        return [2, [get_distance(id1, id2), lower_slope, higher_slope]]
    elif (x2 < x1 and y2 < y1):
        lower_slope = calculate_slope(x1,y1, x2-0.5, y2+0.5)
        higher_slope = calculate_slope(x1,y1, x2+0.5, y2-0.5)
        return [3, [get_distance(id1, id2), lower_slope, higher_slope]]
    elif (x2 > x1 and y2 < y1):
        lower_slope = calculate_slope(x1,y1, x2-0.5, y2-0.5)
        higher_slope = calculate_slope(x1,y1, x2+0.5, y2+0.5)
        return [4, [get_distance(id1, id2), lower_slope, higher_slope]]
    elif (x2 == x1 and y2 > y1):
        lower_slope = calculate_slope(x1,y1, x2-0.5, y2)
        higher_slope = calculate_slope(x1,y1, x2+0.5, y2)
        return [5, [get_distance(id1, id2), lower_slope, higher_slope]]
    elif (x2 < x1 and y2 == y1):
        lower_slope = calculate_slope(x1,y1, x2, y2+0.5)
        higher_slope = calculate_slope(x1,y1, x2, y2-0.5)
        return [6, [get_distance(id1, id2), lower_slope, higher_slope]]
    elif (x2 == x1 and y2 < y1):
        lower_slope = calculate_slope(x1,y1, x2+0.5, y2)
        higher_slope = calculate_slope(x1,y1, x2-0.5, y2)
        return [7, [get_distance(id1, id2), lower_slope, higher_slope]]
    elif (x2 > x1 and y2 == y1):
        lower_slope = calculate_slope(x1,y1, x2, y2-0.5)
        higher_slope = calculate_slope(x1,y1, x2, y2+0.5)
        return [8, [get_distance(id1, id2), lower_slope, higher_slope]]

# Function for getting the ids of the unit squares in the sensing range of a sensor with id
def sensing_range(id):
    x, y = get_coordinate(id)
    ids = []
    for i in range(-sense_radius, sense_radius+1):
        for j in range(-sense_radius, sense_radius+1):
            if (i**2 + j**2 <= sense_radius**2):
                if (x+i >= 0 and x+i < width and y+j >= 0 and y+j < height):
                    ids.append((x+i) + (y+j)*width)
    return ids

# Function for finding the blocking intervals of a sensor with id
def find_blocking_intervals(id, black_id_list):
    if(id not in black_id_list):
        interval_list = [[],[],[],[],[],[],[],[]]
        for black_id in black_id_list:
            interval = get_relative_slope_interval(id, black_id)
            interval_list[interval[0]-1].append(interval[1])
        return interval_list

# Function for checking if a sensor with id1 can sense a sensor with id2
def is_sensible_in_range(id1, id2, block_interval_list):
    quarter = get_relative_slope_interval(id1, id2)[0]
    distance = get_distance(id1, id2)
    x1, y1 = get_coordinate(id1)
    x2, y2 = get_coordinate(id2)
    slope = calculate_slope(x1, y1, x2, y2)
    if(quarter not in [5,7]):
        if(block_interval_list[quarter-1] != []):
            for interval in block_interval_list[quarter-1]:
                if ((slope > interval[1] and slope < interval[2]) and (distance >= interval[0])):
                    return False
                else:
                    return True
        else:
            return True
    else:
        if(block_interval_list[quarter-1] != []):
            for interval in block_interval_list[quarter-1]:
                if((slope < interval[1] or slope > interval[2]) and (distance >= interval[0])):
                    return False
                else:
                    return True
        else:
            return True

# Function for getting the set of sensible ids of a sensor with id
def get_sensible_id_set(id, sense_range_list, block_interval_list):
    if(id not in black_ids):
        sensible_id_set = set()
        sensible_id_set.add(id)
        for sense_id in sense_range_list:
            if (sense_id != id and sense_id not in black_ids):
                if (is_sensible_in_range(id, sense_id, block_interval_list)):
                    sensible_id_set.add(sense_id)
        return sensible_id_set

# Function for getting the distance to the closest sensor from a unit square with id
def get_distance_to_closest_sensor(id):
    min_distance = math.inf
    for sensor_id in sensor_placed_ids:
        distance = get_distance(id, sensor_id)
        if (distance < min_distance):
            min_distance = distance
    return min_distance

# Class for representing a unit square in the area
class Cell:
    def __init__(self, id):
        self.id = id
        if(id not in black_ids):
            self.ids_in_sense_range = sensing_range(id) # ids of the unit squares in the sensing range of the cell
            self.black_ids_in_sense_range = [i for i in self.ids_in_sense_range if (i in black_ids)] # ids of the black unit squares in the sensing range of the cell
            self.blocking_intervals = find_blocking_intervals(id, self.black_ids_in_sense_range) # blocking intervals of the cell
            self.sensible_ids = get_sensible_id_set(id, self.ids_in_sense_range, self.blocking_intervals) # ids of the unit squares that can be sensed by the cell
            self.num_sensible_ids = len(self.sensible_ids) # number of the unit squares that can be sensed by the cell
            self.closest_sensor_distance = get_distance_to_closest_sensor(id) # distance to the closest sensor from the cell

    # For the purpose of using the cells in a priority queue, the less than operator is overloaded
    def __lt__(self, other):
        if (self.num_sensible_ids == other.num_sensible_ids):
            return -(self.closest_sensor_distance) < -(other.closest_sensor_distance)
        return -(self.num_sensible_ids) < -(other.num_sensible_ids)

# Function for checking if a unit square with id is placeable for a sensor    
def is_placeable(id):
    if(id in black_ids or id in sensor_placed_ids):
        return False
    else:
        for sensor_id in sensor_placed_ids:
            if(get_distance(id, sensor_id) < sense_radius*min_sep_length):
                return False
        return True

# Function for updating the sensible id lists of the cells after a sensor is placed
def update_sensible_id_lists():
    for id in range(width*height):
        if(id not in black_ids):
            x,y = get_coordinate(id)
            grid[y][x].sensible_ids = grid[y][x].sensible_ids.difference(covered_ids)
            grid[y][x].num_sensible_ids = len(grid[y][x].sensible_ids)
            grid[y][x].closest_sensor_distance = get_distance_to_closest_sensor(id)

# Function for calculating the coverage of the sensors
def calculate_coverage():
    return (len(covered_ids)/(width*height - len(black_ids)))*100

# Random obstacle generation inside the area starts here
# Random black ids are generated with random starting points and random lengths in random specified directions according to lengths
random_black_ids = set()
while(random_black_ids.__len__() < max_number_of_black_ids):
    for i in range(rock_number):
        rock_length = uniform_select(1, max_rock_length)
        first_black_id = uniform_select(0, width*height-1)
        random_black_ids.add(first_black_id)
        x,y = get_coordinate(first_black_id)
        movement = [0,0]
        for j in range(rock_length-1):
            if(x == 0):
                if(y == 0):
                    movement = [[1,0],[0,1]][uniform_select(0,1)]
                elif(y == height-1):
                    movement = [[1,0],[0,-1]][uniform_select(0,1)]
                else:
                    movement = [[1,0],[0,1],[0,-1]][uniform_select(0,2)]
            elif(x == width-1):
                if(y == 0):
                    movement = [[-1,0],[0,1]][uniform_select(0,1)]
                elif(y == height-1):
                    movement = [[-1,0],[0,-1]][uniform_select(0,1)]
                else:
                    movement = [[-1,0],[0,1],[0,-1]][uniform_select(0,2)]
            else:
                if(y == 0):
                    movement = [[1,0],[-1,0],[0,1]][uniform_select(0,2)]
                elif(y == height-1):
                    movement = [[1,0],[-1,0],[0,-1]][uniform_select(0,2)]
                else:
                    movement = [[1,0],[-1,0],[0,1],[0,-1]][uniform_select(0,3)]
            x, y = update_coordinates(x, y, movement)
            random_black_ids.add(get_id(x, y))

random_black_ids = list(random_black_ids)
while(len(random_black_ids) > max_number_of_black_ids):
    random_index = uniform_select(0, len(random_black_ids)-1)
    random_black_ids.pop(random_index)
# Here random generated obstacles are assigned to the black_ids list
black_ids = random_black_ids

# Please provide the wanted black_id list here if you want to use a specific obstacle configuration under this line
# black_ids = []
# Please note that black_ids should be specified as a list data type

# Random obstacle generation inside the area ends here

# Initialization of the grid with cells
grid = [[Cell(y * width + x) for x in range(width)] for y in range(height)]

# Initialization of the priority queue with cells
cell_queue = []
for y in range(height):
    for x in range(width):
        cell = grid[y][x]
        if(cell.id not in black_ids):
            heapq.heappush(cell_queue, cell)

# Main loop for placing sensors in the area
# Algorithm is explained in the report
temp_cell_list = []
rejected_cell_count = 0
while(max_num_of_sensors > 0 and rejected_cell_count < (width*height) - (black_ids.__len__() + sensor_placed_ids.__len__())):
    if(covered_ids.__len__() == width*height - black_ids.__len__()):
        break
    top_cell = heapq.heappop(cell_queue)
    if(is_placeable(top_cell.id)):
        sensor_placed_ids.append(top_cell.id)
        covered_ids = covered_ids.union(top_cell.sensible_ids)
        update_sensible_id_lists()
        # now dequeue and queue all cells that are not black and not covered
        while(cell_queue.__len__() > 0):
            temp_cell_list.append(heapq.heappop(cell_queue))
        for cell in temp_cell_list:
            heapq.heappush(cell_queue, cell)
        temp_cell_list.clear()
        max_num_of_sensors -= 1
    else:
        rejected_cell_count += 1
        continue

# Print the results, you can print other results you want to see here at the end of the program
print("Coverage: ", calculate_coverage())
print("Number of sensors placed: ", sensor_placed_ids.__len__())
print("Sensor placed ids: ", sensor_placed_ids)