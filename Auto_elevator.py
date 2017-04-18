__author__ = 'chashekh'

import sys
from random import randint
import unittest

class Request:

    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.currentfloor = src

class Elevator:

    def __init__(self, id, max_capacity, num_floors):
        self.id = id
        self.max_capacity = max_capacity
        self.direction = 0
        self.currentfloor = 0
        self.enqued_requests = []
        self.num_floors = num_floors

    def getin(self,request):
        self.enqued_requests.append(request)

    def getout(self):
        outlist = []
        inlist = []
        for i, request in enumerate(self.enqued_requests):
            outlist.append(request) if request.dst == self.currentfloor else inlist.append(request)

        self.enqued_requests = inlist
        for req in outlist:
            print( "Request fullfilled %d %d " %(req.src, req.dst))

    def stationary(self):
        return self.direction == 0

    def empty(self):
        return len(self.enqued_requests) == 0

    def maxcapacity(self):
        return len(self.enqued_requests) == self.max_capacity

    def Elevator_status(self, status):
        if status == 0:
            return "stationary"
        if status == 1:
            return "UP"
        if status == -1:
            return "Down"

        return "Invalid State"

class elev_scheduling:

    def __init__(self):
        pass

    def req_direction(self, src, dst):
        '''

        :param src:
        :param dst:
        :return: 1 if request for UP, -1 for Down, and zero for same floor
        '''
        if src == dst:
            return 0
        return 1 if src < dst else -1

    def request_direction(self, req):
        return self.req_direction(req.src, req.dst)

    def elev_direction(self, elevator, request):

        if elevator.currentfloor == request.src:
            return True

        return  elevator.direction == self.req_direction(elevator.currentfloor, request.src)

    def distance(self, elevator, request):
        '''

        :param elevator:
        :param request:
        :return: distance of elevator's current floor to this request's source
        '''
        dist = abs(elevator.currentfloor - request.src)
        if self.elev_direction(elevator, request) or elevator.direction ==0:
            return dist
        else:
            return sys.maxint

    def check_if_pickup(self, elevator, req):
        '''
            Conditions:
                eleavtor is on same floor as person request floor
                AND (elevator is stationary OR going in same direction as person request)
                AND elevator is not fulll

        :param elevator:
        :param req:
        :return: True if we should allow this person to get in els False
        '''
        return (req.src == elevator.currentfloor and (self.req_direction(req.src, req.dst) == elevator.direction \
                or elevator.direction == 0) and not elevator.maxcapacity())

    def check_if_addtoWait(self, elevator_system, elev_num, request):
        '''
            Conditions:
                Elevator already not at max request capacity
                AND (no one waiting for this
                OR if someone is waiting then they go in same direction)

        :param elevator_system:
        :param elev_num:
        :param request:
        :return: True if we should allow this person to consider for this eleavtor waitlist else False
        '''
        return (len(elevator_system.waitlist[elev_num]) < elevator_system.max_capacity \
            and (len(elevator_system.waitlist[elev_num]) == 0 or
                 self.request_direction(elevator_system.waitlist[elev_num][0]) == self.request_direction(request)))

    def assign(self, request, elevator_system):
        '''
            put this request into this elevator wait queue
            by default we can queue to elevator 1 and deal with it when elevator moves

        :param request:
        :param elevator_system:
        :return: None
        '''
        if request.src < 0 or request.src >= elevator_system.num_floors or \
            request.dst < 0 or request.dst >= elevator_system.num_floors:
                return
        elev_num = 0
        floor_count = sys.maxint

        for i, elevator in enumerate(elevator_system.elevators):
                if self.check_if_addtoWait(elevator_system, i, request):
                    dist = self.distance(elevator, request)
                    if dist < floor_count:
                        elev_num = elevator.id
                        floor_count = dist

        elevator_system.waitlist[elev_num].append(request)


    def schedule(self, elevator_system):
        '''

        :param elevator_system:
        :return: STEP,scheduling policy, Actually picks the people or asks them to look for another elevator
        '''
        for i,elevator in enumerate(elevator_system.elevators):

            if elevator.empty() and len(elevator_system.waitlist[i]) == 0:
                elevator.direction = 0

            newwaitlist = []

            while len(elevator_system.waitlist[i]) > 0:
                req = elevator_system.waitlist[i].pop()
                if self.check_if_pickup(elevator, req):
                            elevator.getin(req)
                            elevator.direction =  self.req_direction(req.src, req.dst)
                else:
                    newwaitlist.append(req)

            for req in newwaitlist:
                self.assign(req, elevator_system)

            if elevator.empty() and len(elevator_system.waitlist[i]) > 0:
                elevator.direction = self.req_direction(elevator.currentfloor, elevator_system.waitlist[i][0].src)

            elevator.currentfloor+=elevator.direction

class ElevatorControlSystem:

    def __init__(self, num_elev, num_floors, max_capacity, elev_scheduling ):
        self.num_elev = num_elev
        self.num_floors = num_floors
        self.max_capacity = max_capacity
        self.elev_scheduling = elev_scheduling
        self.elevators = [Elevator(i, max_capacity, num_floors) for i in range(num_elev)]
        self.waitlist=[[] for i in range(num_elev)]

    def step(self):
        for i,elevator in enumerate(self.elevators):
            elevator.getout()

        self.elev_scheduling.schedule(self)

    def elev_request(self, src, dst):
        r = Request(src, dst)
        self.elev_scheduling.assign(r, self)

    def showwaitlist(self):
        print("Wait List: ")
        print("===============================================================================")
        for i, waitlist in enumerate(self.waitlist):
            print ("Elevator %d : " %(i)),
            for task in waitlist:
                print("(Floor %d to %d) " %(task.src, task.dst)),
            print(" ")

    def showelevatorstatus(self):

        print("\nRequest Serving List")
        print("===============================================================================")
        for i, elevator in enumerate(self.elevators):
            print ("Elevator %d, Floor: %s Direction: %s" %(i, elevator.currentfloor, elevator.Elevator_status(elevator.direction)))
            for j, req in enumerate(elevator.enqued_requests):
                print("(Req %d: Floor %d to %d) "  %(j, req.src, req.dst))
            print("")
    def show(self):
        self.showwaitlist()
        self.showelevatorstatus()

class TestElevator(unittest.TestCase):

    def test_elevator(self):
        s = elev_scheduling()
        num_elev = 3
        num_floors = 5
        max_capacity = 2
        max_steps = 20
        i = 0;
        e = ElevatorControlSystem(num_elev, num_floors, max_capacity, s)
        for i in range(max_steps):

            src = randint(0,num_floors-1)
            dst = randint(0,num_floors-1)
            if src != dst:
                print("New Request Source %s Dest %s" % (src, dst))
                e.elev_request(src, dst)
                e.step()
                e.show()
        while True:
            running = False
            for i in range(len(e.elevators)):
                elevator = e.elevators[i]
                waitlist = e.waitlist[i]
                if len(elevator.enqued_requests) > 0 or len(waitlist) > 0:
                    running = True
                    e.step()
            e.show()
            if not running:
                break




if __name__ == "__main__":
    unittest.main()


