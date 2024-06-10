width, height = 900, 600
size = 30
current_position = [0,0]
grid = []
for i in range(int(round(height / size))):
    grid.append(['#'] * (int(round(width / size))))

for i in range(len(grid)):
    for j in range(len(grid[i])):
        print(grid[i][j], end=' ')
    print()