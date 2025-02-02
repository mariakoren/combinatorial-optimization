from scipy.optimize import linprog

obj = [-1, -2]
#      ─┬  ─┬
#       │   └┤ Coefficient for y
#       └────┤ Coefficient for x
lhs_ineq = [[ 2,  1],  # Red constraint left side
            [-4,  5],  # Blue constraint left side
            [ 1, -2]]  # Yellow constraint left side
rhs_ineq = [20,  # Red constraint right side
            10,  # Blue constraint right side
             2]  # Yellow constraint right side

lhs_eq = [[-1, 5]]  # Green constraint left side
rhs_eq = [15]       # Green constraint right side

bnd = [(0, float("inf")),  # Bounds of x
     (0, float("inf"))]  # Bounds of y

opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,
              A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,
               method="revised simplex")

print(opt)

#   opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,
#  message: Optimization terminated successfully.
#  success: True
#   status: 0
#      fun: -16.818181818181817
#        x: [ 7.727e+00  4.545e+00]
#      nit: 3