from pyquadkey2 import quadkey
import time

# The lat long coordinates of Big Ben pulled from Google Maps
big_ben_lat_long = (51.500752147795716, -0.12463100110988065)
# The lat long coordinates of the Burj Khalifa pulled from Google Maps
burj_khalifa_lat_long = (25.197258440146513, 55.27452867387456)


# Using the pyquadkey2 library, we can find the corresponding quadkey for this location
big_ben_qk = quadkey.from_geo(big_ben_lat_long, 22) # 031313131130102103
burj_khalifa_qk = quadkey.from_geo(burj_khalifa_lat_long, 22) #123023130322311221

# We can view the quadkeys here...
#Big Ben: https://ecn.t3.tiles.virtualearth.net/tiles/a031313131130102103.jpeg?g=129

#Burj Khalifa: https://ecn.t3.tiles.virtualearth.net/tiles/a123023130322311221.jpeg?g=129

# To calculate the distance between quadkeys, we need to understand their relation to each other, whilst also taking into account their level of detail.
# For each added level of detail (LoD), if the other quadkeys value is a column/row over, it is 2^LoD-1 number of squares over

# Calculating Horizontal Distance
def find_distance_horizontally(qk1, qk2):
    # Used to handle different length quadkeys.
    min_len = min(len(str(qk1)), len(str(qk2)))

    # Truncate either quadkey if required and reverse it.
    qk1 = str(qk1)[:min_len][::-1]
    qk2 = str(qk2)[:min_len][::-1]

    # Initalise distance variable
    distance = 0

    for i in range(len(qk1)):
        # qk1 is EVEN and qk2 is ODD. Left -> Right
        if (int(qk1[i]) % 2 == 0) and (int(qk2[i]) % 2 != 0):
            distance += pow(2, i)
        # qk1 is ODD and qk2 is EVEN. Right -> Left
        elif (int(qk1[i]) % 2 != 0) and (int(qk2[i]) % 2 == 0):
            distance -= pow(2, i)
         
    return abs(distance)
start_time = time.time()
print("Horizontal Distance:", find_distance_horizontally(big_ben_qk, burj_khalifa_qk), "Execution Time: ", time.time() - start_time)

# Calculating Vertical Distance
def find_distance_vertical(qk1, qk2):
    # Used to handle different length quadkeys.
    min_len = min(len(str(qk1)), len(str(qk2)))

    # Truncate either quadkey if required and reverse it.
    qk1 = str(qk1)[:min_len][::-1]
    qk2 = str(qk2)[:min_len][::-1]

    # Initalise distance variable
    distance = 0

    for i in range(len(qk1)):
        if (int(qk1[i]) <= 1) and (int(qk2[i]) > 1):
            distance += pow(2, i)
        elif (int(qk1[i]) > 1) and (int(qk2[i]) <= 1):
            distance -= pow(2, i)
    
    return abs(distance)

start_time = time.time()
print("Vertical Distance:", find_distance_vertical(big_ben_qk, burj_khalifa_qk), "Execution Time: ", time.time() - start_time)
