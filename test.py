from CONS import SCREEN_DATA

RESOLUTION = SCREEN_DATA["RESOLUTION"]
X_MAX = RESOLUTION[0]
Y_MAX = RESOLUTION[1]
neighbors_dict = {}

neighbors_dict[(0, 0)] = [(0, 1), (1, 0), (1, 1)]
neighbors_dict[(0, Y_MAX - 1)] = [(0, Y_MAX - 1), (1, Y_MAX - 1), (1, X_MAX - 1)]
neighbors_dict[(X_MAX - 1, 0)] = [(Y_MAX - 1, 0), (X_MAX - 1, 1), (Y_MAX - 1, 1)]


for x in range(X_MAX):
    for y in range(Y_MAX):
        key = (x, y)
        if key not in neighbors_dict:
            neighbors_dict[key] = []
        if x == 0 and y != Y_MAX - 1:
            for ix in range(0, 2):
                for iy in range(-1, 2):
                    if not (ix == 0 and iy == 0):
                        neighbors_dict[key].append((x + ix, y + iy))
        elif y == 0 and x != X_MAX - 1:
            for ix in range(-1, 2):
                for iy in range(0, 2):
                    if not (ix == 0 and iy == 0):
                        neighbors_dict[key].append((x + ix, y + iy))
        else:
            for ix in range(-1, 2):
                for iy in range(-1, 2):
                    if not (ix == 0 and iy == 0):
                        neighbors_dict[key].append((x + ix, y + iy))

        # print(f"x={x},y={y}")


# for key, value in neighbors_dict.items():
#     print(f"{key}: {value}")

x = 10
y = 10

print(neighbors_dict[(x, y)])
