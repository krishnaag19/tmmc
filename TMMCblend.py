import sys

def TMMC():

    def getline(): #Shorthand for getting the lines
        return sys.stdin.readline().strip()
    
    l = getline() #Reading N
    while not l:
        l = getline()
    N = int(l)

    #GRID CONSTRUCTION
    cellsize = 100 #Subgrid Size
    points = [] #Satellite coordinates
    grid = {}

    for i in range(N):
        x,y = map(float,getline().split())
        points.append((x,y))

        cell_x = int(x//cellsize)
        cell_y = int(y//cellsize)
        cell = (cell_x,cell_y)

        if cell not in grid:
            grid[cell] = [] #Adding the cell in the grid
        grid[cell].append(i) #0-based indexing of the satellites

    #DENSITY COMPUTATION
    density_scores = [0]*N
    radius_sq = 100.0*100.0

    for i in range(N):
        px, py = points[i]
        cell_x = int(px // cellsize)
        cell_y = int(py // cellsize)
        
        count = 0
        
        #Looking for satellites in the given and neighbouring subgrids
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                neighbor_cell = (cell_x + dx, cell_y + dy)
                
                if neighbor_cell in grid:
                    for neighbor_idx in grid[neighbor_cell]:
                        if neighbor_idx == i:
                            continue
                            
                        nx, ny = points[neighbor_idx]
                        dist_sq = (px - nx)**2 + (py - ny)**2 #Using square to avoid square root operation
                        
                        if dist_sq <= radius_sq:
                            count += 1
                            
        density_scores[i] = count #Assigning the density in the list for the satellites

    D_max = max(density_scores) #Calculating the max density of a point for normalization required in the future
    if D_max == 0:
        D_max = 1

    Q = int(getline()) #Reading the number of anomalies
    active_satellites = set() #Set of active satellites

    #Searching for potential candidates for assignment
    for i in range(Q):
        cx, cy, r = map(float,getline().split())
        r_sq = r*r

        candidates = []
        active_candidate = -1

        #Looking into the given and neighbouring subgrids
        min_cx = int((cx-r)//cellsize)
        max_cx = int((cx+r)//cellsize)
        min_cy = int((cy-r)//cellsize)
        max_cy = int((cy+r)//cellsize)

        for grid_x in range(min_cx,max_cx+1):
            for grid_y in range(min_cy,max_cy+1):
                cell = (grid_x,grid_y)


                if cell in grid:
                    for idx in grid[cell]:
                        px, py = points[idx]
                        dist_sq = (px - cx)**2 + (py - cy)**2 #Checking whether the satellite lies in the radius of the anomaly

                        if dist_sq <= r_sq:
                            candidates.append(idx)

                            if idx in active_satellites:
                                active_candidate = idx

        #Selection process for the best possible satellite according to our parameters 
        chosen_idx = -1
        if active_candidate != -1: #Assigning a activated satellite right away if it exist in the radius
            chosen_idx = active_candidate
        else:
            best_score = -float('inf') #Setting the main parameter

            for idx in candidates:
                px,py = points[idx]

                dist_to_center_sq = (px - cx)**2 + (py - cy)**2 #Calculating the distance
                normalized_distance = 1.0 - (dist_to_center_sq/r_sq) #Normalizing the distance
                
                density = density_scores[idx] #Taking the pre-computed density
                normalized_density = 1.0 - (density/D_max) #Normalizing our density

                #Computation of the density of activated satellites within a fixed neighbourhood
                d_active = 0
                candidate_cell_x = int(px//cellsize)
                candidate_cell_y = int(py//cellsize)

                #Using the same hashed grids approach
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        neighbour_cell = (candidate_cell_x + dx,candidate_cell_y + dy)
                        if neighbour_cell in grid:
                            for neighbour_idx in grid[neighbour_cell]:
                                if (neighbour_idx != idx) and (neighbour_idx in active_satellites):
                                    nx, ny = points[neighbour_idx]

                                    if (px - nx)**2 + (py - ny)**2 <= radius_sq:
                                        d_active += 1
                
                normalized_active_density = 1.0/(1.0 + d_active) #Normalizing the density of activated satellites

                #Applying the score formula
                score = 0.5*(normalized_distance) + 0.3*(normalized_active_density) + 0.2*(normalized_density)

                if score > best_score: #Choosing the best satellite according to our score parameter
                    best_score = score
                    chosen_idx = idx

        active_satellites.add(chosen_idx)
        print(chosen_idx) #Output command
        
        sys.stdout.flush()


if __name__ == "__main__":
    TMMC()

