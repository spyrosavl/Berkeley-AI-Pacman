from heapq import *

class PriorityQueue():

	def __init__(self):
		self.heap = []
		self.count = 0

	def push(self, item, priority):
		self.count+=1
		entry = [priority, item]
		return heappush(self.heap, entry)

	def pop(self):
		self.count-=1
		return heappop(self.heap)[1] if self.count>=0 else None

	def isEmpty(self):
		return self.count==0
		
	def update(self,item,priority):
		for item in self.heap :
			if item[1] == item and item[0] > priority :
				item[0] = priority
				return heapify(self.heap)
		return self.push(item, priority)

def PQSort(integers):
	q = PriorityQueue()
	new_list = []
	#insert integers into priority queue
	for i in integers :
		q.push(i, i)
		print q.heap
	#pop integers and insert them in new list sorted
	while q.isEmpty() == False :
		print q.heap
		new_list.append(q.pop())

	return new_list