'''
pardis ghavami - 9717023147
HW2 - Q5 implementation
rush hour puzzel
'''
import sys
import copy

class State:
    def __init__(self, board):
        self.board = copy.deepcopy(board)
        self.set_details()
        self.parent = None
        self.depth = 0

    def set_details(self):
        cars = set()
        for i in self.board:
            for j in i:
                cars.add(j)

        cars.remove('.')
        length = {}
        row = {}
        col = {}
        dir = {}
        for ch in cars:
            count = 1
            changed_dir = False
            for i in self.board:
                for j, value in enumerate(i):
                    if value == ch:
                        if count == 1:
                            row[ch] = self.board.index(i)
                            col[ch] = j
                        else:
                            length[ch] = count
                        count += 1
                        if changed_dir:
                            dir[ch] = 'v'
                        else:
                            dir[ch] = 'h'
                if count > 1:      
                    changed_dir = True
        self.cars = cars
        self.length = length
        self.row = row
        self.col = col
        self.dir = dir
           

    def change_board(self, i, j, value):
        self.board[i][j] = value
        self.set_details()

    def is_GOAL(self):
        if self.dir['r'] == 'h':
            if self.col['r'] + self.length['r'] == len(self.board[0]):
                return True
        elif self.dir['r'] == 'v':
            if self.row['r'] + self.length['r'] == len(self.board):
                return True
        return False
    
    def __eq__(self, other):
        return self.board == other.board and self.row == other.row and self.col == other.col and self.cars == other.cars and self.length == other.length and self.dir == other.dir
    
    def __hash__(self):
        return hash((tuple(i) for i in self.board))

def parse_board(string_board):
    return [list(line) for line in string_board.strip().splitlines()]

def expand(s):
    children = []
    for ch in s.cars:
        if s.dir[ch] == 'h':
            board_f = copy.deepcopy(s.board)    #moving forward
            i = s.row[ch]
            j = s.col[ch]
            c = s.col[ch] + s.length[ch]
            dots = 0
            while c < len(s.board[0]) and s.board[i][c] == '.':
                dots += 1
                c += 1
            if(dots >= 1):
                for x in range(dots):
                    for l in range(s.length[ch] - 1, -1, -1):
                        board_f[i][j+l+1] = ch
                        board_f[i][j+l] = '.'
                    j += 1
                new_s = State(board_f)
                new_s.parent = s
                new_s.depth = s.depth + 1
                children.append(new_s)
                
                

            board_b = copy.deepcopy(s.board)     #moving backward
            i = s.row[ch]
            j = s.col[ch]
            c =  s.col[ch] - 1
            dots = 0
            while c >= 0 and s.board[i][c] == '.':  
                dots += 1
                c -= 1
            if(dots >= 1):
                for x in range(dots):
                    for l in range(s.length[ch]):
                        board_b[i][j+l-1] = ch
                        board_b[i][j+l] = '.'
                    j -= 1
                new_s = State(board_b)
                new_s.parent = s
                new_s.depth = s.depth + 1
                children.append(new_s)

        elif s.dir[ch] == 'v':
            board_d = copy.deepcopy(s.board)    #moving down
            i = s.row[ch]
            j = s.col[ch]
            c =  s.row[ch] + s.length[ch]
            dots = 0
            while c < len(s.board) and s.board[c][j] == '.':
                dots += 1
                c += 1
            if(dots >= 1):
                for x in range(dots):
                    for l in range(s.length[ch] - 1, -1, -1):
                        board_d[i+l+1][j] = ch
                        board_d[i+l][j] = '.'
                    i += 1
                new_s = State(board_d)
                new_s.parent = s
                new_s.depth = s.depth + 1
                children.append(new_s)

            board_u = copy.deepcopy(s.board)     #moving up
            i = s.row[ch]
            j = s.col[ch]
            c =  s.row[ch] - 1
            dots = 0
            while c >= 0 and s.board[c][j] == '.':  
                dots += 1
                c -= 1
            if(dots >= 1):
                for x in range(dots):
                    for l in range(s.length[ch]):
                        board_u[i + l - 1][j] = ch
                        board_u[i + l][j] = '.'
                    i -= 1
                new_s = State(board_u)
                new_s.parent = s
                new_s.depth = s.depth + 1
                children.append(new_s)

    return children
            
def ids(board):
    l = 0
    while True:
        result = dfs(board,l)
        if result is not "cutoff":
            return result
        l += 1

def dfs(board, l):
    frontier = list()
    expanded = set()
    result = None
    frontier.append(board)
    while frontier:
        s = frontier.pop()
        if s.is_GOAL():
            return s
        if s.depth > l:
            result = "cutoff"
        else:
            expanded.add(s)
            children = expand(s)
            for child in children:
                if child not in expanded:
                    frontier.append(child)
    return result
def print_path(goal):
    path = []
    path.append(goal)
    parent = goal.parent
    while parent:
        path.append(parent)
        parent = parent.parent
    i = 1
    while i <= len(path):
        s = path[len(path) - i]
        print(i , "\n")
        i += 1
        for r in s.board:
            print(r , "\n")

def main():
    lis= parse_board(sys.stdin.read())
    start = State(lis)
    goal = ids(start)
    print_path(goal)


if __name__ == '__main__':
    main()