import sys

def TMMC():

    def getline(): #Shorthnd for getting the lines
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
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                neighbor_cell = (cell_x + dx, cell_y + dy)
                
                if neighbor_cell in grid:
                    for idx in grid[neighbor_cell]:
                        if idx == i:
                            continue
                            
                        nx, ny = points[idx]
                        dist_sq = (px - nx)**2 + (py - ny)**2
                        
                        if dist_sq <= radius_sq:
                            count += 1
                            
        density_scores[i] = count


    Q = int(getline())
    active_satellites = set()

    for i in range(Q):
        cx, cy, r = map(float,getline().split())
        r_sq = r*r

        candidates = []
        active_candidate = -1

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
                        dist_sq = (px - cx)**2 + (py - cy)**2

                        if dist_sq <= r_sq:
                            candidates.append(idx)

                            if idx in active_satellites:
                                active_candidate = idx

        chosen_idx = -1
        if active_candidate != -1:
            chosen_idx = active_candidate
        else:
            best_density = 0
            best_dist = float('inf')

            for idx in candidates:
                px,py = points[idx]
                dist_to_center_sq = (px - cx)**2 + (py - cy)**2
                density = density_scores[idx]

                if density > best_density:
                    best_density = density
                    best_dist = dist_to_center_sq
                    chosen_idx = idx

                elif density == best_density:
                    if dist_to_center_sq < best_dist:
                        best_dist = dist_to_center_sq
                        chosen_idx = idx


                
        active_satellites.add(chosen_idx)
        # print(chosen_idx)
        sys.stdout.flush()
    print(len(active_satellites))

if __name__ == "__main__":
    try:
        sys.stdin = open("output.txt", "r")
        # Optional: Redirect output to a result file
        # sys.stdout = open("results.txt", "w")
        
        TMMC()
        
    except FileNotFoundError:
        print("Error: 'input.txt' not found. Run the generator first!")

