
# **Introduction:**

This Python tool imports XDATCAR files and calculates the distance between atoms in 3D space while accounting for periodic boundary conditions. It can plot histograms of the interatomic distances and save the results to a log file.

# **Installation:**

To install the program, run the following command in the terminal:
python setup.py install

# **Usage:**

To use the program, run the following command in the terminal:

python map.py <file_path> <min_boundry> <max_boundry>

where file_path is the path to the XDATCAR file, min_boundry is the minimum distance (in Angstroms), and max_boundry is the maximum distance (in Angstroms).

![image](https://user-images.githubusercontent.com/28690072/219899818-6de2837c-92c7-4350-9610-510649db102c.png)


The program will output a set of histograms showing the distribution of interatomic distances between different atom types. These histograms will also be saved in a new directory called log_files/run_x, where x is a unique identifier for each run.

# **Preview**

![image](https://user-images.githubusercontent.com/28690072/219899904-e101fae6-a07a-4c17-b373-742970186979.png)
