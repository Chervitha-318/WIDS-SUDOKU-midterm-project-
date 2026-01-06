"""
sudoku_solver.py

Implement the function `solve_sudoku(grid: List[List[int]]) -> List[List[int]]` using a SAT solver from PySAT.
"""

from pysat.formula import CNF
from pysat.solvers import Solver
from typing import List

def solve_sudoku(grid: List[List[int]]) -> List[List[int]]:
    """Solves a Sudoku puzzle using a SAT solver. Input is a 2D grid with 0s for blanks."""
    cnf = CNF()

    def v(r, c, val):
        return (r * 81) + (c * 9) + val

    for r in range(9):
        for c in range(9):
            cnf.append([v(r, c, val) for val in range(1, 10)])

    for r in range(9):
        for c in range(9):
            for v1 in range(1, 10):
                for v2 in range(v1 + 1, 10):
                    cnf.append([-v(r, c, v1), -v(r, c, v2)])

    for r in range(9):
        for val in range(1, 10):
            cnf.append([v(r, c, val) for c in range(9)])

    for c in range(9):
        for val in range(1, 10):
            cnf.append([v(r, c, val) for r in range(9)])

    for box_r in range(3):
        for box_c in range(3):
            for val in range(1, 10):
                clause = []
                for r in range(box_r * 3, (box_r + 1) * 3):
                    for c in range(box_c * 3, (box_c + 1) * 3):
                        clause.append(v(r, c, val))
                cnf.append(clause)
                
    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                cnf.append([v(r, c, grid[r][c])])

    with Solver(bootstrap_with=cnf) as solver:
        if solver.solve():
            model = solver.get_model()
            result = [[0 for _ in range(9)] for _ in range(9)]
            for lit in model:
                if lit > 0:
                    idx = lit - 1
                    val = (idx % 9) + 1
                    col = (idx // 9) % 9
                    row = idx // 81
                    result[row][col] = val
            return result
        else:
            return [] 

def print_pretty(solution: List[List[int]]):
    if not solution:
        print("No solution found!")
        return
    
    border = "+-------+-------+-------+"
    for r in range(9):
        if r % 3 == 0:
            print(border)
        row_str = "| "
        for c in range(9):
            row_str += str(solution[r][c]) + " "
            if (c + 1) % 3 == 0:
                row_str += "| "
        print(row_str)
    print(border)

# Example Usage
if __name__ == "__main__":
    example_grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    solved = solve_sudoku(example_grid)
    print_pretty(solved)
    # TODO: implement encoding and solving using PySAT
    pass