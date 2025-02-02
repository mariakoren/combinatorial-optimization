from scipy.optimize import linprog

obj = [5, 8]

lhs_ineq = [[-10, -1], 
            [-1, -10], 
            [ -10, -10]] 
rhs_ineq = [-100,  
            -200,  
             -300]  


bnd = [(0, float("inf")), 
     (0, float("inf"))]  

opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,
              bounds=bnd,
               method="revised simplex")

print(opt)