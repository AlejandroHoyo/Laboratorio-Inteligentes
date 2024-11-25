from __future__ import annotations
import h5py
from dataclasses import dataclass
import numpy as np
import math


@dataclass
class Dataset:
    xinf: float
    yinf: float
    xsup: float
    ysup: float
    cellsize: int   
    nodata_value: float

# Transform functions
def mean_func(cells):
    return np.mean(cells)

def max_func(cells):
    return np.max(cells)

def min_func(cells):
    return np.min(cells)

class Map:
    def __init__(self, filename):  # Initialize the values of the map
        self.f = h5py.File(filename, 'r')
        self.nodata_value = None
        self.size_cell = None
        self.up_left = None
        self.down_right = None
        self.dim = None
        self.datasets = []  

        # Initialize variables to store min and max coordinates
        min_xinf = float('inf')
        min_yinf = float('inf')
        max_xsup = float('-inf')
        max_ysup = float('-inf')

        for dataset_name in self.f:  # Search the datasets
            dataset = self.f[dataset_name]
            self.nodata_value = dataset.attrs["nodata_value"]
            self.size_cell = dataset.attrs["cellsize"]
            min_xinf = min(min_xinf, dataset.attrs["xinf"])
            min_yinf = min(min_yinf, dataset.attrs["yinf"])
            max_xsup = max(max_xsup, dataset.attrs["xsup"])
            max_ysup = max(max_ysup, dataset.attrs["ysup"])

            dataset_attrs = Dataset(  # Set the attributes of the dataset
                dataset.attrs["xinf"],
                dataset.attrs["yinf"],
                dataset.attrs["xsup"],
                dataset.attrs["ysup"],
                dataset.attrs["cellsize"],
                dataset.attrs["nodata_value"])

            dataset_attrs.name = dataset_name
            self.datasets.append(dataset_attrs)

        # Calculate the dimensions of the map
        rows = math.ceil((max_ysup - min_yinf) / self.size_cell)
        columns = math.ceil((max_xsup - min_xinf) / self.size_cell)
        self.dim = (rows, columns)
        self.up_left = (min_yinf, min_xinf)
        self.down_right = (max_ysup, max_xsup)
        
    def resize(self, factor, transform, name): 
        new_cellsize = self.size_cell * factor
        new_f = h5py.File(f"{name}.hdf5", "w")
        attributes_to_copy = ['xinf', 'xsup', 'yinf', 'ysup', 'nodata_value']  # List of attribute names to copy

        for dataset_name in self.f:  # Search the datasets
            current_dataset_grid = self.f[dataset_name]
            new_grid_rows = math.ceil(current_dataset_grid.shape[0] / factor)
            new_grid_columns = math.ceil(current_dataset_grid.shape[1] / factor)
            new_dataset_grid = new_f.create_dataset(dataset_name, (new_grid_rows, new_grid_columns), dtype=current_dataset_grid.dtype)

            for attr_name in attributes_to_copy:
                if attr_name in current_dataset_grid.attrs:
                    new_dataset_grid.attrs[attr_name] = current_dataset_grid.attrs[attr_name]
            new_dataset_grid.attrs["cellsize"] = new_cellsize

            for i in range(0, new_grid_rows):
                for j in range(0, new_grid_columns):
                    cells = current_dataset_grid[i * factor:(i + 1) * factor, j * factor:(j + 1) * factor]
                    cells_without_nodata_value = cells[cells != self.nodata_value]
                    new_dataset_grid[i, j] = transform(cells_without_nodata_value) if cells_without_nodata_value.size > 0 else self.nodata_value

        new_map = Map(f"{name}.hdf5")  
        return new_map
    
    
    def umt_YX(self, y, x) -> float:  
        """ Find the height of the given y x coordinates""" 
        for current_dataset in self.datasets:  
            if (current_dataset.xinf <= x <= current_dataset.xsup
                    and current_dataset.yinf <= y <= current_dataset.ysup):
                # Convert Y and X coordinates to row and column
                row = (current_dataset.ysup - y + 1) // self.size_cell
                col = (x - current_dataset.xinf + 1) // self.size_cell
                data_grid = self.f[current_dataset.name]
                value = data_grid[row, col]
                return value
                # Return the nodata value if the coordinates are outside the map or no valid data is found
        return self.nodata_value
        
    def close(self):
        self.f.close()  
