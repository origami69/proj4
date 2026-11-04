# comment: this is A simplified process control block using the variables we have and added a mutable data section afer the comment
#name,arrival,exec,priority,tools,allowed
class PCB:
    # immutable data
    name: str
    arrival: int
    exec: int
    priority: int
    tools: list
    allowed: list
    # mutable data, we do this so we dont change execution time directly and still have it since Waiting time needs it later
    remaining: int
    startTime: int
    status: bool

    def __init__(self, name, arrival, exec, priority, tools, allowed):
        self.name = name
        self.arrival = arrival
        self.exec = exec
        self.priority = priority
        self.tools = tools
        self.allowed = allowed
        self.remaining = exec
        self.startTime = -1
        self.status = set(tools).issubset(set(allowed)) # as long as everything in tools is in ALlowed its true thus Tools must be a subset  of Allowed


#I know list can handle reallocations itself but I have specific requuirements for capacity so I used the code Above which I
# Made in CS 310 or the datastructures and algorithims class
class QueueF:
    front: int
    back: int
    count: int
    capacity: int
    my_list: list
    def __init__(self, sizer):
        self.front = 0
        self.back = -1
        self.count = 0
        if sizer < 2:
            sizer = 2
        findPow = 2
        while sizer > findPow:
            findPow *= 2
        self.capacity = findPow
        self.my_list = [None] * findPow
    def push_b(self, agent):
        if self.count == self.capacity:
            newSize = self.capacity * 2
            newList = [None] * newSize
            for i in range(self.count):
                newList[i] = self.my_list[(self.front + i) & (self.capacity-1)]
            self.my_list = newList
            self.front = 0
            self.back = self.count - 1
            self.capacity = newSize
        self.back = (self.back + 1) & (self.capacity - 1)
        self.my_list[self.back] = agent
        self.count += 1
    def get_h(self):
        if self.count < 1:
            return -1
        getVal = self.my_list[self.front]
        self.front = (self.front + 1) & (self.capacity - 1)
        self.count -= 1
        return getVal
    def peek_Arrival(self):
        if self.count < 1:
            return -1
        getVal = self.my_list[self.front]
        return getVal.arrival
#this is the ordering you gave us so it better be like this in the csv
#file must come first in input everything else doesnt matter as much when it comes to order
# file --a fcfs --q 2 --cs 1
#the default settings are q=2, cs=2 and fcfs
#I expect commas for seperation so use that please in the csv file in this format exactly, also use comma even if you dont have any tools or allowed
#name,arrival,exec,priority,tools,allowed
#then for if you have multiple then seperate tools like this
#tool1;tool2;tool3
#then you also do the same thing for allowed
#tool1;tool2;tool3
def main():
    commander = input().lower()
    words = commander.split()
    fileLoc = words[0]
    quantum = 2
    algo = "fcfs"
    contextCost = 2
    counter = 0
    while counter < len(words):
        if words[counter] == "--algo":
            algo = words[counter + 1]
            counter += 1
        elif words[counter] == "--q":
            quantum = int(words[counter + 1])
            counter += 1
        elif  words[counter] == "--cs":
            contextCost = int(words[counter + 1])
            counter += 1
        counter += 1
    theList = []
    size = 0
    with open(fileLoc, 'r') as file:
        #to help me know order
        # name,arrival,exec,priority,tools,allowed
        for line in file:
            size += 1
            row1 = line.strip().lower().split(',')
            row2 = row1[4].split(';')
            row3 = row1[5].split(';')
            startPcb = PCB(row1[0], int(row1[1]), int(row1[2]), int(row1[3]), row2, row3)
            theList.append(startPcb)
    #now we sort this fucking shit, I will use the pyhon sort built in since it uses a powersort which is better than what I plannned of using a quicksort anyway this isnt a algorithims class
    #anywaay I do sortiing since I dont trusy you will put everything in order by arrival time so I will sort it myself then put to ready queue
    #http://stackoverflow.com/questions/31942169/python-sort-array-of-arrays-by-multiple-conditions this helped me learn more about the python sorting
    tuple(theList)
    #so we sort first by arrival then the priority
    sorter = lambda x: (x.arrival, x.priority)
    sorted_l = sorted(theList, key=sorter)
    theQueue = QueueF(size)
    counter = 0
    while counter < size:
        theQueue.push_b(sorted_l[counter])
        counter += 1
    if algo == "fcfs":
        first_come(theQueue, contextCost, size)
    elif algo == "rr":
        round_robin(theQueue, quantum, contextCost, size)
    else:
        print("Input Error: please put in fcfs or rr for the --algo")
        return

def round_robin(theQueue, quantum, contextCost, size):
    holdPcb = theQueue.get_h()
    clock = 0
    contextAmount = 0
    turnAroundAvg = 0
    waitingAvg = 0
    responseAvg = 0
    ready_queue  = QueueF(size)
    print("===  RR  ===");
    print(
        "Name", "Arrival", "Burst", "Priority", "Completion",
        "Waiting", "Turnaround", "Response", "Status")
    while holdPcb != -1:
        if holdPcb.startTime < 0:
            holdPcb.startTime = clock
        if holdPcb.remaining <= quantum:
            clock += holdPcb.remaining
            turnAround = clock - holdPcb.arrival
            waiting = turnAround - holdPcb.exec
            response = holdPcb.startTime - holdPcb.arrival
            print(
                holdPcb.name, holdPcb.arrival, holdPcb.exec, holdPcb.priority, clock,
                waiting, turnAround, response, holdPcb.status)
            turnAroundAvg += turnAround
            waitingAvg += waiting
            responseAvg += response
            #we add all task from sortyed queue to readu queue if their arrival time is greater than clock or equal to
            while theQueue.peek_Arrival() != -1 and clock >= theQueue.peek_Arrival():
                ready_queue.push_b(theQueue.get_h())
        else:
            holdPcb.remaining -= quantum
            clock += quantum
            #we add all task from sortyed queue to readu queue if their arrival time is greater than clock or equal to
            while theQueue.peek_Arrival() != -1 and clock >= theQueue.peek_Arrival():
                ready_queue.push_b(theQueue.get_h())
            ready_queue.push_b(holdPcb)
        #mpw we either get from ready queue but if thats empty we should  also check if the next arrival is very lonng way than our current clock
        #imagine if out currrent clock is 10 but the next task is 100 , so its inportabt ti waut
        if ready_queue.peek_Arrival() != -1:
            holdPcb = ready_queue.get_h()
        else:
            #this is wheere the waiting happens right before the context sqwitch
            clock = max(clock,theQueue.peek_Arrival())
            holdPcb = theQueue.get_h()
        clock += contextCost
        contextAmount += 1
    if contextAmount == 0:
        contextAmount += 1
    print("Context count: ", contextAmount - 1)
    print("TurnAround Average: ", turnAroundAvg / size)
    print("Waiting Average: ", waitingAvg / size)
    print("ResponseTime Average: ", responseAvg / size)
    return


def first_come(theQueue, contextCost, size):
    holdPcb = theQueue.get_h()
    clock = 0
    contextAmount = 0
    turnAroundAvg = 0
    waitingAvg = 0
    responseAvg = 0
    print("===  FCFS  ===");
    print(
          "Name", "Arrival", "Burst", "Priority", "Completion",
          "Waiting", "Turnaround", "Response", "Status")
    while holdPcb != -1:
        # We should wait here till the next task comes in here then do context switch since we only do switch once our boi arrives
        clock = max(clock, theQueue.peek_Arrival())
        turnAround = ((holdPcb.exec + clock) - holdPcb.arrival)
        waiting =  turnAround - holdPcb.exec
        response = clock - holdPcb.arrival
        print(
               holdPcb.name, holdPcb.arrival, holdPcb.exec, holdPcb.priority,holdPcb.exec + clock,
               waiting,turnAround, response, holdPcb.status)
        contextAmount += 1
        turnAroundAvg += turnAround
        waitingAvg += waiting
        responseAvg += response
        clock += holdPcb.exec
        # We should wait here till the next task comes in here then do context switch since we only do switch once our boi arrives
        clock = max(clock, theQueue.peek_Arrival())
        clock += contextCost
        holdPcb = theQueue.get_h()
    if contextAmount == 0:
        contextAmount += 1
    print("Context count: ", contextAmount - 1)
    print("TurnAround Average: ", turnAroundAvg / size)
    print("Waiting Average: ", waitingAvg / size)
    print("ResponseTime Average: ", responseAvg / size)
    return

if __name__ == "__main__":
    main()