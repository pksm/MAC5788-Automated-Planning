@ECHO OFF
echo.
echo 'Solving pddl/satellite/problems/pfile01.pddl ...'
echo.
py pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile01.pddl --heuristics %1 
echo.
echo 'Solving pddl/satellite/problems/pfile02.pddl ...'
py pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile02.pddl --heuristics %1 
echo.

echo 'Solving pddl/satellite/problems/pfile03.pddl ...'
py pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile03.pddl --heuristics %1 
echo.

echo 'Solving pddl/satellite/problems/pfile04.pddl ...'
py pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile04.pddl --heuristics %1 
echo.

echo 'Solving pddl/satellite/problems/pfile05.pddl ...'
py pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile05.pddl --heuristics %1 
echo.

echo 'Solving pddl/satellite/problems/pfile06.pddl ...'
py pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile06.pddl --heuristics %1 
echo.

echo 'Solving pddl/satellite/problems/pfile07.pddl ...'
py pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile07.pddl --heuristics %1 
echo.

echo 'Solving pddl/satellite/problems/pfile08.pddl ...'
py pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile08.pddl --heuristics %1 
echo.

echo 'Solving pddl/satellite/problems/pfile09.pddl ...'
py pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile09.pddl --heuristics %1 
echo.

echo 'Solving pddl/satellite/problems/pfile10.pddl ...'
py pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile10.pddl --heuristics %1 
echo.
