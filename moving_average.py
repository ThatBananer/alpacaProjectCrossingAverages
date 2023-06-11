"""Class for calculating the moving average."""
from linked_list import LinkedList

class MovingAverage:
    def __init__(self, time_period_days):
        self.time_period_days = time_period_days
        self.linked_list = self.__createLinkedList()
        self.movingAvg = 0
        self.movingAvgSum = 0


    # ---- public methods ---- #

    # get moving avg
    def getMA(self):
        if self.movingAvg == 0:
            print("MA is 0 in getMA")
            return 0
        return self.movingAvg

    # add new day data point
    # needs to: get find new avg, delete oldest val if at limit, add newest val to front
    def addNewDataPoint(self, newVal):
        self.__calcNewMA(newVal)

    # print moving average
    def printMA(self):
        print(f"Avg: {self.movingAvg}\tAvgSum: {self.movingAvgSum}")

    # ---- private methods ---- #

    # calc new avg
    def __calcNewMA(self, newVal):
        self.linked_list.newHead(newVal)
        self.movingAvgSum += newVal
        if self.linked_list.length == self.time_period_days:
            self.movingAvgSum -= self.linked_list.tail.data
            self.linked_list.delete_tail()

        if self.movingAvg == 0:
            self.movingAvg = newVal
        else:
            self.movingAvg = self.movingAvgSum / self.linked_list.length

    # linked list creation
    def __createLinkedList(self):
        return LinkedList()

    # ...
