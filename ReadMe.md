# Read Me
 This is the instruction of the program for COMP 472 assignment 1
### introduction
This program running in terminal or IDE. There are two program file (.py) in this program and a folder called Shape which include all the maps shape file.
### Running this program
To run this program require Python 3.7 and some libraries which listed in library section.
You can run this program in terminal or IDE. I recommend using IDE to run this program, because the zip file including all the library or python environment. If you using terminal, you may need to install some library.
If you meet running requirement, you can just simply run `run.py` file.
If you want to change the variable of this program. You can find them in `run.py` `def main()` section `# variables`. You can change `size_of_each_coordianates` and `threshold_of_crime`. By default `size_of_each_coordianates = 0.002` and `threshold_of_crime = 0.17`.
### Structure
This program have two python files which are `run.py` and `func.py`.
The `run.py` including the main function which included the variables.
The `func.py` including the all the function we need in `run.py` file.
### run.py file
1. It will read shape file get all the crime data.
2. Create maps image which show all the data on maps
3. Execute find path function, which can find the shortest path between start and end point.
4. Display the path.
### func.py file
1. Function `move_point_to_intersection_point`: it can move the point on intersection point if the point is not on the intersection point of the maps.
2. Function `get_distance`: it can calculate the distance between the current point to the end point.
3. Function `check_point_at_edge`: it can check the point whether on the edge of the maps.
4. Function `check_shortest_path`: check the current path whether is the shortest path.
5. There are 8 moving function `up, right, down, left, up_right, down_right, down_left, up_left`
6. Function `find_path`: This is the most important function to find the shortest path. The algorithm will be introduced in algorithm section.
### Algorithm
1. Read shape file and get crime data.
2. Create maps and display the crime num on maps
3. Move start and end point on intersection point if they are not on intersection point.
4. Using A\* algorithm to find the shortest path.
	1. There are `open_list, close_list, shortest_path_list`
		1. `open_list` store the points that available for the check and sorted by distance to the end point + the cost from start point.
		2. `close_list` store all the points which have already checked.
		3. `shortest_path_list` store all the point which have already checked and the previous point which is shortest to the start point and the cost from the start point.
	2. There is an infinite loop which will stop if the execution time over 10 second, cannot find path or find the path. The loop will check the first element of `open_list` by using 8 moving functions. If the next point is not on the edge it will skip it. If the point in the `close_list` it will check the cost, if the current is less than the previous cost, it will overlap the previous cost in `shortest_path_list`.
5. We will get a `shortest_path` array from previous step. Program will display it on maps.
### library
1. `numpy`
2. `shapefile`
3. `matplotlib`
4. `time`
5. `decimal`
6. `timeout_decorator`
7. `copy`


