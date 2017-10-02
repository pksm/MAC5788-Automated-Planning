@ECHO OFF
echo.
echo 'Solving pddl/logistics/problems/strips-log-x-1.pddl ...'
echo.
python pystrips.py solve pddl/logistics/domain.pddl pddl/logistics/problems/strips-log-x-1.pddl --heuristics %1 --weight %2

echo.
echo 'Solving pddl/logistics/problems/strips-log-x-2.pddl ...'
echo.
python pystrips.py solve pddl/logistics/domain.pddl pddl/logistics/problems/strips-log-x-2.pddl --heuristics %1 --weight %2

echo.
echo 'Solving pddl/logistics/problems/strips-log-x-5.pddl ...'
echo.
python pystrips.py solve pddl/logistics/domain.pddl pddl/logistics/problems/strips-log-x-5.pddl --heuristics %1 --weight %2
