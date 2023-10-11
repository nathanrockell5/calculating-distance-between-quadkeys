# Calculating the Distance Between Two Quad Keys

## Background

Quadkeys are a method of encoding geographic coordinates into a string of characters, typically numbers, that represent a location at a specific level of detail within a map's tiling system. They are often used in mapping and geospatial applications, such as Geographic Information Systems (GIS).

### How Quadkeys Work:

1. **Dividing the World into Quadrants**: The Earth's surface, typically using the Mercator projection, is divided into a hierarchy of square tiles or quadrants, with each level of the hierarchy representing a different level of detail (zoom level).

2. **Hierarchical Structure**: Each quadrant can be further divided into four smaller quadrants, and this subdivision can continue recursively as you zoom in on a map.

3. **Encoding**: To represent a specific location at a particular zoom level, you use a quadkey, which is a string of characters. Each character in the quadkey represents one level of the quadrant hierarchy, using 0-3 to represent top-left, top-right, bottom-left, and bottom-right, respectively.

4. **Zoom Level**: The length of the quadkey determines the zoom level it represents. A longer quadkey corresponds to a higher zoom level with more detail.

5. **Example**: For example, the quadkey that contains [Big Ben](https://ecn.t3.tiles.virtualearth.net/tiles/a031313131130102103.jpeg?g=129) is '031313131130102103' at a level of detail of 18. Any more precision would not contain the target.



Quadkeys are useful for various purposes, including caching map tiles, identifying map features, and simplifying geospatial calculations. They provide a compact way to represent a location in a hierarchical tiling system, making it easier to work with maps and spatial data in digital applications.

This article demonstrates how to easily find the distance between two quadkeys, returning how far left or right, up or down that quadkey is in relation to the other, regardless of the level of detail.

## Visualisation

| - | - | - | - | - | - | - | - |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
| 002 | 003🏠 | 012 | 013 | 102 | 103 | 112 | 113 |
| 020 | 021 | 030 | 031 | 120🏢 | 121 | 130 | 131 |
| 022 | 023 | 032 | 033 | 122 | 123 | 132 | 133 |
| 200 | 201 | 210 | 211 | 300 | 301 | 310 | 311 |
| 202🚘 | 203 | 212 | 213 | 302 | 303 | 312 | 313 |
| 220 | 221 | 230 | 231 | 320 | 321🏠 | 330 | 331 |
| 222 | 223 | 232 | 233 | 322 | 323 | 332 | 333 |

In this simplified example is a quadkey grid. This can represent a section of a map, we can see that there is:
- 🏠 in 003 and 321
- 🚘 in 202
- 🏢 in 120

If we wanted to find the distance between the two houses 🏠(003) -> 🏠(321)  we can easily see it's **4 Across**, and **5 Down**. However, what if the level of detail was 18? It would be much harder and more tedious to count across.

#### Basic Example

From right -> left of the quadkey, each position, has 2^(LevelOfDetail-1) number of columns/rows within it. Therefore based on the rules below, if we detect that the column/row has moved over for that part of the quadkey, we simply add 2^(LevelOfDetail-1).

##### For Width

- IF QK1 is even AND QK2 is odd, add 2^(LoD-1) to width
- IF QK1 is odd AND QK2 is even, subtract 2^(LoD-1) from width
- ELSE do nothing, as it would still be in the same column.

| 2^2^| 2^1^ | 2^0^ |
| - | - | - |
| 0 | 0 | 3 |
| 3 | 2 | 1 |
| +4| 0 | 0 |
- 0 is even, 3 is odd. +4
- 0 is even, 2 is even. +0
- 3 is odd, 1 is odd. +0
- **Width: 4**

##### For Height

- IF QK1 is <= 1 AND QK2 is > 1, add 2^(LoD-1) to length
- IF QK1 is > 1 AND QK2 is <= 1, subtract 2^(LoD-1) to length
- ELSE do nothing, as it would still be in the same row.

| 2^2^| 2^1^ | 2^0^ |
| - | - | - |
| 0 | 0 | 3 |
| 3 | 2 | 1 |
| +4| +2 | -1 | 
- 0 is <= 1, 3 is >1. +4
- 0 is <= 1, 2 is >1. +2
- 3 is >1, 1 is <= 1. -1
- **Height: 5**

The same result is achieved as above, just by looking at their values compared to the other in the same position.

## The Code

This example uses Python, and the [pyquadkey2](https://pypi.org/project/pyquadkey2/) library to convert between coordinates in the lat long format and quadkeys.

### Step 0: Import Libraries

```python
from pyquadkey2 import quadkey
```

### Step 1: Convert lat long locations into quadkeys.
```python
    # The lat long coordinates of Big Ben pulled from Google Maps
    big_ben_lat_long = (51.500752147795716, -0.12463100110988065)
    # The lat Lng coordinates of the Burj Khalifa pulled from Google Maps
    burj_khalifa_lat_long = (25.197258440146513, 55.27452867387456)

    # Using the pyquadkey2 library, we can find the corresponding quadkey for this location
    big_ben_qk = quadkey.from_geo(big_ben_lat_long, 18) # 031313131130102103
    burj_khalifa_qk = quadkey.from_geo(burj_khalifa_lat_long, 18) #123023130322311221
```
We can view the quadkeys here:
[Big Ben Quadkey - 031313131130102103](https://ecn.t3.tiles.virtualearth.net/tiles/a031313131130102103.jpeg?g=129)
[Burj Khalifa Quadkey - 123023130322311221](https://ecn.t3.tiles.virtualearth.net/tiles/a123023130322311221.jpeg?g=129) 

### Step 2: Finding Distance Horizontally

```python
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
            
        # +1 to include quadkey of origin
        return abs(distance)
    
    print("Horizontal Distance:", find_distance_horizontally(big_ben_qk, burj_khalifa_qk)) #40340
```

### Step 3: Finding Distance Vertically
```python
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
    
    print("Vertical Distance:", find_distance_vertical(big_ben_qk, burj_khalifa_qk)) #24925
```
### Big O Notation
The loop inside the code iterates a maximum of min_len times, which is constant. Therefore, regardless of the length of the input quadkeys, the time complexity remains constant because the number of iterations in the loop does not depend on the input size.

So, in this specific context where min_len is a constant representing the level of detail, you can express the time complexity as O(1).

## Conclusion
Thank you for taking the time to look through this short article. I hope you found it interesting and/or useful! If you have any questions about what was covered, please feel free to contact me on my LinkedIn.

- LinkedIn: https://www.linkedin.com/in/nathan-rockell/
- GitHub: https://github.com/nathanrockell5
- Source Code: https://github.com/nathanrockell5/calculating-distance-between-quadkeys
