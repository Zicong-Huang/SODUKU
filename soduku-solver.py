import numpy as np


class Cell(object):
    def __init__(self, irow, icol, num):
        self.cell_index = (irow, icol)
        self.block_index = (irow // 3, icol // 3)
        self.number = num
        self.candidates = []
        self.num_candidates = 0
        self.occupied = (num != 0)

    def fill_number(self, num):
        if num != 0 and not self.occupied:
            self.number = num
            self.candidates = []
            self.num_candidates = 0
            self.occupied = True
        else:
            raise ValueError('Not filled.')

    def set_candidates(self, num_list):
        self.candidates = num_list
        self.num_candidates = len(self.candidates)

    def confirm_candidates(self):
        if self.num_candidates == 1 and not self.occupied:
            self.number = self.candidates[0]
            self.candidates = []
            self.num_candidates = 0
            self.occupied = True
            return True
        else:
            return False

    def __repr__(self):
        return str(self.number)


class Soduku(object):
    def __init__(self, puzzle_txt):
        self.source = puzzle_txt
        self.raw_puzzle = np.loadtxt(puzzle_txt, delimiter=',', dtype='int')
        self.puzzle = self.init_cell()

    def init_cell(self):
        puzzle = np.empty((9, 9), dtype='object')
        for irow in range(9):
            for icol in range(9):
                num = self.raw_puzzle[irow, icol]
                puzzle[irow, icol] = Cell(irow, icol, num)
        return puzzle

    def show(self, version='original'):
        if version == 'original':
            p = self.raw_puzzle
        elif version == 'solved':
            self.solver()
            p = self.puzzle
        else:
            raise ValueError('Wrong Inpupt. Set version to \'original\' or \'solved\'')
        sep = '+-------+-------+-------+'
        print()
        print('      SODUKU PUZZLE      ')
        print(version)
        print(sep)
        for irow in range(9):
            r_str = '| ' + \
                    ' | '.join(str(p[irow, 3*i])+' '+str(p[irow, 3*i+1])+' '+str(p[irow, 3*i+2]) for i in range(3)) +\
                    ' |'
            print(r_str)
            if irow in [2, 5, 8]:
                print(sep)
        print('* From: ', self.source)
        if version == 'solved' and not self.is_completed():
            print('** The puzzle is ' + str(['NOT ', ''][self.is_completed()]) + 'completed.')

    def get_block(self, block_irow, block_icol):
        irow = block_irow * 3
        icol = block_icol * 3
        return self.puzzle[irow: irow + 3, icol: icol + 3]

    def get_row(self, irow):
        return self.puzzle[irow, :]

    def get_col(self, icol):
        return self.puzzle[:, icol]

    def get_cell(self, irow, icol):
        return self.puzzle[irow, icol]

    def check_in_row(self, irow, num):
        return num in [x.number for x in self.get_row(irow).flatten()]

    def check_in_col(self, icol, num):
        return num in [x.number for x in self.get_col(icol).flatten()]

    def check_in_block(self, irow, icol, num):
        block_irow = irow // 3
        block_icol = icol // 3
        block = self.get_block(block_irow, block_icol).flatten()
        return num in [x.number for x in block]

    def check_num_valid(self, irow, icol, num):
        if not self.get_cell(irow, icol).occupied and \
                not self.check_in_row(irow, num) and \
                not self.check_in_col(icol, num) and \
                not self.check_in_block(irow, icol, num):
            return True
        else:
            return False

    def set_cell(self, irow, icol, num):
        if self.check_num_valid(irow, icol, num):
            self.get_cell(irow, icol).fill_number(num)
        else:
            raise ValueError('This number is not valid.')

    def is_completed(self):
        plain_puzzle = self.puzzle.flatten()
        return 0 not in [x.number for x in plain_puzzle]

    def set_cell_candidates(self, irow, icol):
        candidate_list = list()
        for i in range(1, 10):
            if self.check_num_valid(irow, icol, i):
                candidate_list.append(i)
        self.get_cell(irow, icol).set_candidates(candidate_list)

    def set_all_candidates(self):
        for irow in range(9):
            for icol in range(9):
                self.set_cell_candidates(irow, icol)

    def solver_elimination(self):
        applied = False
        while not self.is_completed():
            changes = 0
            self.set_all_candidates()
            for irow in range(9):
                for icol in range(9):
                    curr_cell = self.get_cell(irow, icol)
                    changes += curr_cell.confirm_candidates()
                    if changes > 0:
                        applied = True
            if changes == 0:
                break
        return applied

    def solver_row_unique_candidate(self):
        self.set_all_candidates()
        change = 0
        for irow in range(9):
            row = self.get_row(irow).flatten()
            candidate_position = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
            for icol in range(9):
                cell = row[icol]
                for candidate in cell.candidates:
                    candidate_position[candidate].append(icol)
            for candidate, position in candidate_position.items():
                if len(position) == 1:
                    self.set_cell(irow, position[0], candidate)
                    change += 1
        return change > 0

    def solver_col_unique_candidate(self):
        self.set_all_candidates()
        change = 0
        for icol in range(9):
            col = self.get_col(icol).flatten()
            candidate_position = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
            for irow in range(9):
                cell = col[irow]
                for candidate in cell.candidates:
                    candidate_position[candidate].append(irow)
            for candidate, position in candidate_position.items():
                if len(position) == 1:
                    self.set_cell(position[0], icol, candidate)
                    change += 1
        return change > 0

    def solver_block_unique_candidate(self):
        self.set_all_candidates()
        change = 0
        for block_irow in range(3):
            for block_icol in range(3):
                block = self.get_block(block_irow, block_icol).flatten()
                candidate_position = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
                for pos in range(9):
                    cell = block[pos]
                    for candidate in cell.candidates:
                        candidate_position[candidate].append(pos)
                for candidate, position in candidate_position.items():
                    if len(position) == 1:
                        pos = position[0]
                        in_block_row = pos // 3
                        in_block_col = pos % 3
                        irow = in_block_row + block_irow * 3
                        icol = in_block_col + block_icol * 3
                        self.set_cell(irow, icol, candidate)
                        change += 1
        return change > 0

    def solver(self):
        while not self.is_completed():
            applied = 0
            applied += self.solver_elimination()
            applied += self.solver_row_unique_candidate()
            applied += self.solver_col_unique_candidate()
            applied += self.solver_block_unique_candidate()
            if applied == 0:
                break
        return self.puzzle


if __name__ == '__main__':
    '''---easy---'''
    test_easy = '../SODUKU/soduku1-easy.txt'
    test_easy = Soduku(test_easy)
    test_easy.show('original')
    test_easy.show('solved')
    '''---medium---'''
    test_medium = '../SODUKU/soduku3-medium.txt'
    test_medium = Soduku(test_medium)
    test_medium.show('original')
    test_medium.show('solved')
    '''---hard---'''
    test_hard = '../SODUKU/soduku4-hard.txt'
    test_hard = Soduku(test_hard)
    test_hard.show('original')
    test_hard.show('solved')
    '''---expert---'''
    test_expert = '../SODUKU/soduku5-expert.txt'
    test_expert = Soduku(test_expert)
    test_expert.show('original')
    test_expert.show('solved')
