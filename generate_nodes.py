class Node:
    goal_state=[0,0,1]
    number_of_instances=0

    def __init__(self, parent,state):
        self.parent=parent
        self.state=state
        Node.number_of_instances+=1


    def __str__(self):
        return str(self.state)

    def goal_test(self):
        if self.state==self.goal_state:
            return True
        return False

    def is_valid(self):
        M=self.state[0]
        C=self.state[1]
        B=self.state[2]

        if M>=0 and M<=3 and C<=3 and C>=0:
            return True

        else:
            return False

    def is_killed(self):
        M=self.state[0]
        C=self.state[1]
        if M<C and M>0:
            return True
        if M>C and M<3:
            return True


    def generate_child(self):
        children = []
        b = 1  # boat in right shore
        o = -1
        if self.state[2] == 1:
            b = 0  # boat in left shore
            o = 1
        for x in range(3):
            for y in range(3):
                new_state = self.state.copy()
                new_state[0], new_state[1], new_state[2] = new_state[0] + o * x, new_state[1] + o * y, b
                new_node = Node(self, new_state)
                if new_node.is_valid() and (x + y >= 1 and x + y <= 2):
                    children.append(new_node)

        return children

    def find_path(self):
        path = []
        path.append(self.state)
        parent = self.parent
        while parent != None:
            path.append(parent.state)
            parent = parent.parent
        return path