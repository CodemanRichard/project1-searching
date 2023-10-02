from queue import PriorityQueue
import numpy as np

MISMATCH_COST = 5
GAP_COST = 3


class AStarSolver_3:
    def __init__(self, seqs):
        self.seqs = seqs
        self.visited = np.zeros(shape=(len(seqs[0])+1, len(seqs[1])+1, len(seqs[2])+1), dtype=bool)
        self.queue = PriorityQueue()
        self.init_node = AStarNode(0, (0,0,0), None, self)
        self.end_node = None
        self.match_cost = 0

    def solve(self):
        """Find the minimum match cost between three sequences"""
        self.queue.put(self.init_node)
        while True:
            cur_node = self.queue.get()
            if cur_node.is_target():
                self.end_node = cur_node
                self.match_cost = cur_node.cost
                return self.match_cost
            else:
                for node in cur_node.expand():
                    self.queue.put(node)

    def align_seq(self):
        """Return the aligned sequences of three input sequences"""
        seq1 = ""
        seq2 = ""
        seq3 = ""
        cur_node = self.end_node
        next_pos = None
        cur_pos = None
        while next_pos != (0,0,0):
            next_pos = cur_node.parent.pos
            cur_pos = cur_node.pos
            if cur_pos[0]==next_pos[0]:
                seq1 += '*'
            else:
                seq1 += self.seqs[0][cur_pos[0]-1]
            if cur_pos[1]==next_pos[1]:
                seq2 += '*'
            else:
                seq2 += self.seqs[1][cur_pos[1]-1]
            if cur_pos[2]==next_pos[2]:
                seq3 += '*'
            else:
                seq3 += self.seqs[2][cur_pos[2]-1]
            cur_node = cur_node.parent
        return (seq1[::-1], seq2[::-1], seq3[::-1])


    
class AStarNode:
    def __init__(self, cost, pos, parent, solver):
        """Initialization of an A* node"""
        self.cost = cost
        self.pos = pos
        self.parent = parent
        self.solver = solver
        self.heuristic_cost = self.heuristic()
        self.evaluated_cost = self.cost + self.heuristic_cost

    def __lt__(self, other):
        """Comparison between two A* nodes"""
        self.evaluated_cost = self.cost + self.heuristic()
        other.evaluated_cost = other.cost + other.heuristic()
        return self.evaluated_cost < other.evaluated_cost

    # need to implement another heuristic function
    def heuristic(self):
        """The heuristic function of A*"""
        # h(n)定义为两条序列剩下部分长度之差乘上匹配空隙的代价
        # 对于三序列匹配，进行两两比对
        len_1 = len(self.solver.seqs[0]) - (self.pos[0]+1)
        len_2 = len(self.solver.seqs[1]) - (self.pos[1]+1)
        len_3 = len(self.solver.seqs[2]) - (self.pos[2]+1)
        return GAP_COST * (abs(len_1-len_2) + abs(len_1-len_3) + abs(len_2-len_3))

    def is_target(self):
        """Return if the node has reached the terminate condition"""
        return (self.pos[0]==len(self.solver.seqs[0]) 
                and self.pos[1]==len(self.solver.seqs[1])
                and self.pos[2]==len(self.solver.seqs[2]))

    def Node(self, cost, pos):
        """Return a child node of the current node"""
        return AStarNode(cost, pos, self, self.solver)

    def expand(self):
        """Return all nodes that can be expanded to"""
        if self.solver.visited[self.pos]:
            return []
        else:
            self.solver.visited[self.pos] = True
            expand_nodes = []
            # (x,y,z)->(x+1,y,z)
            if self.pos[0] < len(self.solver.seqs[0]):
                next_pos = (self.pos[0]+1, self.pos[1], self.pos[2])
                expand_nodes.append(self.Node(self.cost+2*GAP_COST, next_pos))
            # (x,y,z)->(x,y+1,z)
            if self.pos[1] < len(self.solver.seqs[1]):
                next_pos = (self.pos[0], self.pos[1]+1, self.pos[2])
                expand_nodes.append(self.Node(self.cost+2*GAP_COST, next_pos))
            # (x,y,z)->(x,y,z+1)
            if self.pos[2] < len(self.solver.seqs[2]):
                next_pos = (self.pos[0], self.pos[1], self.pos[2]+1)
                expand_nodes.append(self.Node(self.cost+2*GAP_COST, next_pos))
            # (x,y,z)->(x+1,y+1,z)
            if self.pos[0] < len(self.solver.seqs[0]) and self.pos[1] < len(self.solver.seqs[1]):
                next_pos = (self.pos[0]+1, self.pos[1]+1, self.pos[2])
                if self.solver.seqs[0][self.pos[0]] == self.solver.seqs[1][self.pos[1]]:
                    expand_nodes.append(self.Node(self.cost+2*GAP_COST, next_pos))
                else:
                    expand_nodes.append(self.Node(self.cost+MISMATCH_COST+2*GAP_COST, next_pos))
            # (x,y,z)->(x+1,y,z+1)
            if self.pos[0] < len(self.solver.seqs[0]) and self.pos[2] < len(self.solver.seqs[2]):
                next_pos = (self.pos[0]+1, self.pos[1], self.pos[2]+1)
                if self.solver.seqs[0][self.pos[0]] == self.solver.seqs[2][self.pos[2]]:
                    expand_nodes.append(self.Node(self.cost+2*GAP_COST, next_pos))
                else:
                    expand_nodes.append(self.Node(self.cost+MISMATCH_COST+2*GAP_COST, next_pos))
            # (x,y,z)->(x,y+1,z+1)
            if self.pos[1] < len(self.solver.seqs[1]) and self.pos[2] < len(self.solver.seqs[2]):
                next_pos = (self.pos[0], self.pos[1]+1, self.pos[2]+1)
                if self.solver.seqs[1][self.pos[1]] == self.solver.seqs[2][self.pos[2]]:
                    expand_nodes.append(self.Node(self.cost+2*GAP_COST, next_pos))
                else:
                    expand_nodes.append(self.Node(self.cost+MISMATCH_COST+2*GAP_COST, next_pos))
            # (x,y,z)->(x+1,y+1,z+1)
            if (self.pos[0] < len(self.solver.seqs[0])
                and self.pos[1] < len(self.solver.seqs[1])
                and self.pos[2] < len(self.solver.seqs[2])):
                next_pos = (self.pos[0]+1, self.pos[1]+1, self.pos[2]+1)
                mismatch_count = 0
                if self.solver.seqs[0][self.pos[0]] != self.solver.seqs[1][self.pos[1]]:
                    mismatch_count += 1
                if self.solver.seqs[1][self.pos[1]] != self.solver.seqs[2][self.pos[2]]:
                    mismatch_count += 1
                if self.solver.seqs[0][self.pos[0]] != self.solver.seqs[2][self.pos[2]]:
                    mismatch_count += 1
                expand_nodes.append(self.Node(self.cost+mismatch_count*MISMATCH_COST, next_pos))
            return expand_nodes