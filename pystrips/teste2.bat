@ECHO OFF
echo.
echo 'Solving pddl/satellite/problems/pfile01.pddl ...'
echo.
python pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile01.pddl --heuristics %1 --weight %2
echo.
echo 'Solving pddl/satellite/problems/pfile02.pddl ...'
python pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile02.pddl --heuristics %1 --weight %2
echo.

echo 'Solving pddl/satellite/problems/pfile03.pddl ...'
python pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile03.pddl --heuristics %1 --weight %2
echo.

echo 'Solving pddl/satellite/problems/pfile04.pddl ...'
python pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile04.pddl --heuristics %1 --weight %2
echo.

echo 'Solving pddl/satellite/problems/pfile05.pddl ...'
python pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile05.pddl --heuristics %1 --weight %2
echo.

echo 'Solving pddl/satellite/problems/pfile06.pddl ...'
python pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile06.pddl --heuristics %1 --weight %2
echo.

echo 'Solving pddl/satellite/problems/pfile07.pddl ...'
python pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile07.pddl --heuristics %1 --weight %2
echo.

echo 'Solving pddl/satellite/problems/pfile08.pddl ...'
python pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile08.pddl --heuristics %1 --weight %2
echo.

echo 'Solving pddl/satellite/problems/pfile09.pddl ...'
python pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile09.pddl --heuristics %1 --weight %2
echo.

echo 'Solving pddl/satellite/problems/pfile10.pddl ...'
python pystrips.py solve pddl/satellite/domain.pddl pddl/satellite/problems/pfile10.pddl --heuristics %1 --weight %2
echo.
