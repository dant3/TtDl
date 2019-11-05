import sys
import builtins as python

enabled = False



def print(*line):
    global enabled
    if enabled:
        python.print(line, file = sys.stderr)
