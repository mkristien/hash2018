
m = None
vehicles = None
rides = None

# Hamiltonian distance of two locations
def dist(a, b):
    result = 0
    result += abs(a[0] - b[0])
    result += abs(a[1] - b[1])
    return result

# what must the ride start for it to be possible to finish on time
def start_t_max(start_loc, end_loc, end_time):
    distance = dist(start_loc, end_loc)
    return end_time - distance

# remove rides that have the latest start time in the past
def remove_old(rides, cur_time):
    count = 0
    for ride in rides:
        if ride.start_t_max < cur_time:
            rides.remove(ride)
            count += 1

    print 'remove old rides', count

def score_ride_per_vehicle(ride, vehicle, cur_time):
    global m
    score = 0
    time_empty = dist(vehicle.cur_pos, ride.start_loc)
    start_t_min = cur_time + time_empty

    if start_t_min <= ride.start_t:
        score += m.bonus

    if start_t_min <= ride.start_t_max:
        score += ride.duration
    return score


'''
returns outdata
'''
def process(indata):
    global m, vehicles, rides
    m, vehicles, rides = indata

    