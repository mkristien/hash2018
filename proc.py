import Queue
from tqdm import tqdm

m = None
vehicles = None
rides = None
cur_time = 0

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
def remove_old():
    global rides, cur_time
    count = 0
    for ride in rides:
        if ride.start_t_max < cur_time:
            rides.remove(ride)
            count += 1
    print 'remove old rides', count

def remove_unreachable():
    global cur_time, rides, vehicles
    to_remove = []
    for ride in rides:
        max_score = 0
        for v in vehicles:
            score = score_ride_per_vehicle(ride, v)
            if score > max_score:
                max_score = score
                break
        if max_score == 0:
            to_remove.append(ride)

    for ride in to_remove:
        rides.remove(ride)
    print 'removed unreachanble', len(to_remove)


def score_ride_per_vehicle(ride, vehicle):
    global m, cur_time
    score = 0
    time_empty = dist(vehicle.cur_pos, ride.start_loc)
    start_t_min = cur_time + time_empty

    if start_t_min <= ride.start_t:
        score += m.bonus

    if start_t_min <= ride.start_t_max:
        score += ride.duration
    return score

def new_time(ride, v):
    global cur_time
    to_start = dist(ride.start_loc, v.cur_pos)
    wait =  ride.start_t - (cur_time + to_start)
    if wait < 0:
        wait = 0
    to_end = ride.duration

    return cur_time + to_start + wait + to_end


# returns [score]
def scores_per_vehicle(vehicle):
    global rides, cur_time
    scores = []
    for ride in rides:
        scores.append(score_ride_per_vehicle(ride, vehicle))
    return scores

def assign_ride(ride, vehicle):
    global rides

    time = new_time(ride,vehicle)

    vehicle.rides.append(ride.id)
    rides.remove(ride)
    return (time, vehicle)

# returns [(new_time, vehicle)]
def assign(vehicles):
    global rides
    result = []
    for v in vehicles:
        scores = scores_per_vehicle(v)
        for i, score in enumerate(scores):
            if score > 0:
                result.append(assign_ride(rides[i], v))
                break
    return result

'''
returns outdata
'''
def process(indata):
    global m, vehicles, rides, cur_time
    m, vehicles, rides = indata

    cur_time, last_remove, last_time = 0, 0, 0
    ride_queue = Queue.PriorityQueue()

    planned_events = assign(vehicles)
    for e in planned_events:
        ride_queue.put(e)

    with tqdm(total=m.T) as pbar:
        while cur_time <= m.T and not ride_queue.empty():
            # Prune the rides list a little
            if cur_time - last_remove > 1000:
                remove_old()
                last_remove = cur_time

            free_vehicles = ride_queue.get()

            if type(free_vehicles) == tuple:
                cur_time = free_vehicles[0]
                planned_events = assign([free_vehicles[1]])
            else:
                cur_time = free_vehicles[0][0]
                planned_events = assign(map(lambda tup: tup[1], free_vehicles))

            for e in planned_events:
                ride_queue.put(e)

            pbar.update(cur_time - last_time)
            last_time = cur_time

    return vehicles
