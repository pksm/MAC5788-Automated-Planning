# This file is part of pypddl-PDDLParser.

# pypddl-parser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pypddl-parser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pypddl-parser.  If not, see <http://www.gnu.org/licenses/>.


import argparse
import time
import signal

from pddlparser import PDDLParser
from planner import ProgressionPlanning
from heuristics import h_naive, h_add, h_max, h_ff


def parse():
    usage = 'python3 main.py <DOMAIN> <INSTANCE>'
    description = 'pypddl-parser is a PDDL parser built on top of ply.'
    parser = argparse.ArgumentParser(usage=usage, description=description)

    parser.add_argument('domain',  type=str, help='path to PDDL domain file')
    parser.add_argument('problem', type=str, help='path to PDDL problem file')
    parser.add_argument('-s', '--search', choices=['depth', 'breadth','astar'],
                        default='depth', type=str, help='Search Type (default=depth)')
    parser.add_argument('-ph', '--heuristics', choices=['naive', 'add', 'max', 'ff'],
                        default='naive', type=str, help='heuristics (default=h_add)')
    #parser.add_argument('-w', '--weight', type=float, default=1.0, help='heuristics weight (default=1.0)')
    parser.add_argument('-v', '--verbose', action='store_true')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse()

    uptime = {}

    start_time = time.time()
    domain  = PDDLParser.parse(args.domain)
    problem = PDDLParser.parse(args.problem)
    end_time = time.time()
    uptime['parsing'] = end_time - start_time
    start_time = time.time()
    planner = ProgressionPlanning(domain, problem)
    end_time = time.time()
    uptime['grounding'] = end_time - start_time

    if args.search == 'depth':
        search = 0
    elif args.search == 'breadth':
        search = 1
    elif args.search == 'astar':
        search = 2

    h = h_naive
    if args.heuristics == 'add':
        h = h_add
    elif args.heuristics == 'max':
        h = h_max
    elif args.heuristics == 'ff':
        h = h_ff

    start_time = time.time()
    #signal.signal(signal.SIGALRM, signal.SIG_DFL)
    #signal.alarm(300)
    solution, explored, visited = planner.solve(search, h) # IMPORTANTE
    #signal.alarm(0)
    end_time = time.time()
    uptime['planning'] = end_time - start_time

    # print statistics
    print('>> solution length =', len(solution))
    print('>> time: parsing = {0:.4f}, grounding = {1:.4f}, planning = {2:.4f}'.format(
        uptime['parsing'], uptime['grounding'], uptime['planning']))
    print('>> nodes explored =', explored)
    print('>> nodes visited  =', visited)
    print('>> ramification factor = {0:.4f}'.format(visited / explored))
    print()

    if args.verbose:
        print('>> Initial state:')
        print(', '.join(sorted(problem.init)))
        print()
        print('>> Solution:')
        print('\n'.join(map(repr, solution)))
        print()
        print('>> Goal state:')
        print(', '.join(sorted(problem.goal)))


# USANDO DEEPCOPY
#python3 -m cProfile -s tottime main.py pddl/blocksworld/domain.pddl pddl/blocksworld/problems/probBLOCKS-04-0.pddl -s astar -ph add

# solution length = 6
# time: parsing = 0.0270, grounding = 0.0012, planning = 17.9456
# nodes explored = 11
# nodes visited  = 21
# ramification factor = 1.9091

# 5430960 function calls (4715384 primitive calls) in 18.073 seconds

# Ordered by: internal time

# ncalls  tottime  percall  cumtime  percall filename:lineno(function)
# 564788/3564    5.289    0.000   15.060    0.004 copy.py:137(deepcopy)
