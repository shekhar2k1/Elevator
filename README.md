Assumption:

1)	Since floor pick/drop info is not given, I am generating source/destination floor and based on that up/down decision is made
2)	People can get in the elevator only it is stationary or going in their desired direction.
3)	Since there can be multiple people/elevator. Each elevator has a max capacity.
4)	No individual function for querying the state of an elevator, Instead each command will show states of all the elevator.

Algorithm:

The solution to select an elevator takes into account people going in only one direction at one time. What it means is Elevators cannot queue up request in both directions.

Let's say elevator A is at level 6 and all elevators others are on level zero
If two requests arrive, Request1: Level5 to Level6 and Request2: Level5 to Level4. Even though elevator A is closer for both of these requests it will pick only one and other will be served by another elevator (Lets' say Elevator B)
If elevator B is still far away by the time Request1 is finished by elevator A and if it closer to serve the second request as well then we reassign Request2 to elevator A.
As soon as a user requests an elevator we put it in wait queue of a particular elevator which is closest at that point of time. Wait queue is just for waiting and it doesn't ensure ride in that particular elevator. Now at each STEP we keep changing the assignment of this request if required (if it is not already served). 


If an elevator has already max capacity people waiting on it we don’t use that elevator for wait queue. If there are more people waiting than capacity, we just queue it to first elevator and handle it when we step through simulation. Entry/Exit time is negligible.

Elevator takes one extra step when reversing direction. 
Elevators go only up till last floor requested in any direction.
Elevators keep waiting at their respective floors when there are no requests.


Implementation:

class Request: Request by a passenger (source and destination information)
class Elevator: Information about particular Elevator (includes id, floor, direction, num of people in this elevator, max capacity of elevator, moving or stationary)
class ElevatorControlSystem: Elevator control sub system. Keeps track of all elevators.
class elev_scheduling: A scheduling algorithm class which can be passed to Elevator subsystem. It makes a decision based on elevator current status, moving direction, current capacity etc.. I am using SCAN algorithm but another elevator scheduling algorithm can be passed. It needs to be subclassed but because of time constraint I did not do it.


I am attaching two files. Both have same code.

Auto_elevator.py: auto generates and runs complete requests and always steps after a request. In the end it steps until it finishes all the requests (20 default).

Manual_elevator.py:
this file needs to be tested manually.
You can specify the parameters like number of elevators or just run it with default params.
Once we run it, only two inputs  are allowed
1)	step
2)	src_int_floor_id1  dst_int_floord_id_2 (two integers separated by space)

All elevator status will be shown after each command.
