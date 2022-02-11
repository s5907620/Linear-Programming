import gurobipy as gp
import numpy as np
from gurobipy import GRB

def CreateVar( m, numOfClient, numOfFacility, open, x ) :
    for i in range( numOfFacility ) :
        open[i] = m.addVar( vtype = GRB.BINARY, name = "open(%s)" %i )
        for j in range( numOfClient ) :
            x[j, i] = m.addVar( vtype = GRB.BINARY, name = "x(%s, %s)" %( j, i ) )
    
    m.update()
# CreateVar end

# main
# declare model
m = gp.Model("facility")

# given cost
facility = [ 2, 3, 4, 3, 5, 2 ]
distance = np.array( [ ( 6, 6, 8, 4, 0, 6 ),
                       ( 6, 8, 6, 0, 6, 6 ),
                       ( 5, 0, 3, 6, 3, 0 ),
                       ( 2, 3, 0, 2, 4, 4 ),
                       ( 8, 6, 8, 3, 2, 0 ),
                       ( 6, 4, 2, 3, 6, 6 ),
                       ( 3, 6, 3, 4, 2, 2 ),
                       ( 3, 2, 2, 3, 4, 2 )
                     ] )

# given index
numOfClient = 8
numOfFacility = 6

# decision value
open, x = {}, {}

CreateVar( m, numOfClient, numOfFacility, open, x )

# constrs.
for j in range( numOfClient ) :
    m.addConstr( gp.quicksum( x[j, i] for i in range( numOfFacility ) ) == 1 )
    
for (j, i) in x :
    m.addConstr( open[i] - x[j, i] >= 0 )

# add constrs. end

# objective
m.setObjective( gp.quicksum( facility[i] * open[i] for i in range( numOfFacility ) ) +
                gp.quicksum( distance[j, i] * x[j, i] for j in range( numOfClient ) for i in range( numOfFacility ) ),
                GRB.MINIMIZE )
# objective end

m.optimize()

# print solution
print( '\nTOTAL COSTS: %g' % m.objVal )

for v in open :
    print( open[v] )
    
print( '\n' )
    
for j in range( numOfClient ) :
    for i in range( numOfFacility ) :
        print( '%s ' %x[j, i] )
    print( '\n' )

# main end
