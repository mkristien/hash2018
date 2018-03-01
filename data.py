class Map(object):
    def __init__(self, rows, cols, no_vehicles, no_rides, bonus, T):
        self.rows = rows
        self.cols = cols
        self.bonus = bonus
        self.T = T


class Vehicle(object):
    def __init__(self):
        self.cur_pos = [0, 0]


class Ride(object):
    def __init__(self, start_x, start_y, end_x, end_y, t_start, t_finish):
        self.start_loc = [start_x, start_y]
        self.end_loc = [end_x, end_y]
        self.start_t = t_start
        self.end_t = t_finish
        self.duration = abs(end_x - start_x) + abs(end_y - start_y)
        self.start_t_max = self.end_t - self.duration


def load(infile):
    ''' Parses infile.

    Returns:
    m - Map object
    vehicles - list of Vehicle objects
    rides - list of Ride objects
    '''
    with open(infile) as f:
        first_line = map(int, f.readline().split())
        m = Map(*first_line)
        vehicles = []
        for _ in range(first_line[2]):
            vehicles.append(Vehicle())

        rides = []
        for ride_line in f.readlines():
            rides.append(Ride(*map(int, ride_line.split())))

    return m, vehicles, rides


def store(outfile, data):
    ''' Accepts output file and output data dictionary
    '''
    pass
