from scipy.optimize import linprog
import sys
obj = [1, 1, 1, 1, 1, 1]

lhs_ineq = [[-1, 0, 0, 0, 0, -1], 
            [-1, -1, 0, 0, 0, 0], 
            [0, -1, -1, 0, 0, 0],
            [0, 0, -1, -1, 0, 0],
            [0, 0, 0, -1, -1, 0],
            [0, 0, 0, 0, -1, -1]] 
rhs_ineq = [-4,  
            -18,  
             -7,
             -15,
             -20,
             -6]  


bnd = [(0, sys.maxsize), 
     (0, sys.maxsize),
     (0, sys.maxsize),
     (0, sys.maxsize),
     (0, sys.maxsize),
     (0, sys.maxsize)]  

opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,
              bounds=bnd,
               method="revised simplex")

print(opt)

# /mnt/c/Users/maria/Desktop/combinatorial-optimization/linearprogramming/ola.py:25: DeprecationWarning: `method='revised simplex'` is deprecated and will be removed in SciPy 1.11.0. Please use one of the HiGHS solvers (e.g. `method='highs'`) in new code.
#   opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,
#  message: The problem appears infeasible, as the phase one auxiliary problem terminated successfully with a residual of 4.7e+01, greater than the tolerance 1e-12 required for the solution to be considered feasible. Consider increasing the tolerance to be greater than 4.7e+01. If this tolerance is unnaceptably large, the problem is likely infeasible.
#  success: False
#   status: 2
#      fun: 2.9082950978024646
#        x: [ 0.000e+00  1.597e+00  9.105e+00  0.000e+00  9.297e+00]
#      nit: 10