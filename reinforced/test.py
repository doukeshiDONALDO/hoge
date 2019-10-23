import random
LEDSTATE = ['white','black','green','red','blue']
class Node():
	MOVE = [2,4,5,6,8,9,0]
	def __init__(self,state=None):
		self.children = []
		self.state = state
		self.record_state = LEDSTATE
                self.value = 0
	def add_child(self):
		chois = random.choice(self.record_state)
		self.record_state.remove(chois)
		child= Node(chois)
		self.children.append(child)
                self.value += 1
	def check_maxchild(self):
		if len(self.children) == len(LEDSTATE):
			return True
		return False
	def __repr__(self):
		return str(self.value)

def addint(node):
	node.add_child()


a = Node() 
print(len(a.MOVE))
addint(a)
#
#a.add_child()
#a.add_child()
#a.add_child()
#a.add_child()
#a.add_child()
