#!/usr/bin/python3
# Auto-tuner prototype
# Built for INE5540 robot overlords

import subprocess # to run stuff
import sys # for args, in case you want them
import time # for time

def tuner(argv):
    exec_file = 'matmult'

    compilation_flags = ['-Ofast', '-O3', '-O2', '-O1']
    compilation_lines = list()
    compile_line = ['gcc', '-o',exec_file,'mm.c']

    for flag in compilation_flags:
    	compilation_lines.append(compile_line + [flag])
    steps_line = '-DSTEP='

    compilation_lines.append(compile_line)
    best_time = sys.maxsize
    best_line = compile_line
    best_step = 2



    for cp_line in compilation_lines:
	    steps = best_step
	    last_time = sys.maxsize

	    compile(cp_line, steps_line + str(steps))
	    time = run(exec_file, best_time)
	    if time < best_time:
	    	best_time = time
	    	best_line = cp_line

	    while time < last_time:
	    	steps *= 2
	    	compile(cp_line, steps_line + str(steps))
	    	last_time = time
	    	time = run(exec_file, best_time)
	    	if time < best_time:
	    		best_time = time
	    		best_line = cp_line
	    		best_step = steps
	    print("-------------")

    print("The best time was: " + str(best_time))
    print("With the following line: " + str(best_line + [steps_line + str(best_step)]))

    return [best_line, steps_line]


    # Compile code

def compile(compilation_line, steps):
    print("\nTesting compilation with: " + str(compilation_line+[steps]))
    compilation_try = subprocess.run(compilation_line+[steps])
    if (compilation_try.returncode == 0):
        print("Happy compilation")
    else:
        print("Sad compilation")

    # Run code

def run(exec_file, best_time):
    input_size = str(9)
    average = 0
    times = 10
    skip_count = 3


    for count in range(times):
	    print("\nStarting run " + str(count))
	    t_begin = time.time() # timed run
	    run_trial = subprocess.run(['./'+exec_file, input_size])
	    t_end = time.time()
	    average+= t_end-t_begin
	    if count > skip_count-1 and best_time < 1.5* average/count:
	    	print("Too slow, skipped other runs")
	    	break

	    print("Time taken: " + str(t_end-t_begin))
    average = average/times
    print("Average of " + str(times) + " runs: " + str(average))
    return average


if __name__ == "__main__":
    tuner(sys.argv[1:]) # go auto-tuner
	