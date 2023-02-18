import math
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

def read_xdatcar(file_path):
    with open(file_path, 'r') as f:
        # Read header lines
        system = f.readline().rstrip('\n')
        scale = float(f.readline().rstrip('\n'))
        arr_1 = np.array([float(s)*scale for s in f.readline().rstrip('\n').split()])
        arr_2 = np.array([float(s)*scale for s in f.readline().rstrip('\n').split()])
        arr_3 = np.array([float(s)*scale for s in f.readline().rstrip('\n').split()])
        v = arr_1[0]
        bounds = [arr_1[0], arr_2[1], arr_3[2]]
        element_names = f.readline().rstrip('\n').split()
        element_numbers = f.readline().rstrip('\n').split()

        # Read positions
        positions = []
        for line in f:
            if 'Direct' in line or 'Cartesian' in line:
                continue
            positions.append([float(x) for x in line.split()])

        # Reshape positions into a dictionary of element lists
        element_lists = {}
        index = 0
        for i, name in enumerate(element_names):
            n_elements = int(element_numbers[i])
            element_lists[name] = positions[index:index+n_elements]
            index += n_elements

    return system, bounds, element_lists


def distance(p1, p2, bounds):
    # Calculate distance w/ periodic boundary
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    dx -= bounds[0] * np.round(dx / bounds[0])
    dy -= bounds[1] * np.round(dy / bounds[1])
    dz -= bounds[2] * np.round(dz / bounds[2])
    return math.sqrt(dx**2 + dy**2 + dz**2)


def find_distances(element_lists, bounds, min_distance, max_distance):
    distances = {}
    for name1, list1 in element_lists.items():
        for name2, list2 in element_lists.items():
            if name1 >= name2:
                continue
            key = name1 + '-' + name2
            d_array = []
            for i, p1 in enumerate(list1):
                for j, p2 in enumerate(list2):
                    d = distance(p1, p2, bounds)
                    if min_distance <= d <= max_distance:
                        d_array.append(d)
            distances[key] = d_array
    return distances


def plot_histograms(distances):
    if not os.path.exists('log_files'):
        os.mkdir('log_files')

    folder_name = 'log_files/run_1'
    run_num = 1
    while os.path.exists(folder_name):
        run_num += 1
        folder_name = f'log_files/run_{run_num}'

    os.mkdir(folder_name)
    with open(f'{folder_name}/results.log', 'w') as f:
        for key, values in distances.items():
            f.write(key + '\n')
            f.write(str(values) + '\n\n')
            plt.hist(values)
            plt.title(key)
            plt.savefig(f'{folder_name}/{key}.png')
            plt.clf()


def main():
    parser = argparse.ArgumentParser(description='Calculate and plot interatomic distances.')
    parser.add_argument('file_path', type=str, help='path to the XDATCAR file')
    parser.add_argument('min_boundry', type=float, help='minimum distance (in Angstroms)')
    parser.add_argument('max_boundry', type=float, help='maximum distance (in Angstroms)')
    args = parser.parse_args()

    system, bounds, element_lists = read_xdatcar(args.file_path)
    distances = find_distances(element_lists, bounds, args.min_boundry, args.max_boundry)
    plot_histograms(distances)

if __name__ == '__main__':
    main()
    