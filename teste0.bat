@echo off
echo.
echo 'Solving blocksworld/problems/probBLOCKS-04-0.pddl ...'
echo.
py main.py pddl/blocksworld/domain.pddl pddl/blocksworld/problems/probBLOCKS-04-0.pddl --search %1 

echo.
echo 'Solving blocksworld/problems/probBLOCKS-04-2.pddl ...'
echo.
py main.py pddl/blocksworld/domain.pddl pddl/blocksworld/problems/probBLOCKS-04-2.pddl --search %1 
