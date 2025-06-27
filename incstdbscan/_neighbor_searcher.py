import numpy as np
from sklearn.neighbors import NearestNeighbors
from sortedcontainers import SortedList


class NeighborSearcher:
    def __init__(self, radius,spatial_radius, metric, p):
        self.neighbor_searcher = \
            NearestNeighbors(radius=radius, metric="cosine")
        self.spatial_neighbor_searcher = \
            NearestNeighbors(radius=spatial_radius, metric="euclidean")
        self.values = np.array([])
        self.points = np.array([])
        self.ids = SortedList()

    def insert(self, new_value,new_point, new_id):
        self.ids.add(new_id)
        position = self.ids.index(new_id)

        self._insert_into_array(new_value, new_point, position)
        self.neighbor_searcher = self.neighbor_searcher.fit(self.values)
        self.spatial_neighbor_searcher = self.spatial_neighbor_searcher.fit(self.points)

    def _insert_into_array(self, new_value, new_point, position):
        extended = np.insert(self.values, position, new_value, axis=0)
        if not self.values.size:
            extended = extended.reshape(1, -1)
        self.values = extended
        extended = np.insert(self.points, position, new_point, axis=0)
        if not self.points.size:
            extended = extended.reshape(1, -1)
        self.points = extended

    def query_neighbors(self, query_value,query_point):
        neighbor_indices = self.neighbor_searcher.radius_neighbors(
            [query_value], return_distance=False)[0]
        spatial_neighbor_indices = self.spatial_neighbor_searcher.radius_neighbors(
            [query_point], return_distance=False)[0]
        # spatial_neighbor_indices_candidate = self.spatial_neighbor_searcher.radius_neighbors(
        #     [np.array([0.0,0.0])], return_distance=False)[0]
        # spatial_neighbor_indices=np.unique(np.concatenate((spatial_neighbor_indices, spatial_neighbor_indices_candidate)))
        neighbor_indices=np.intersect1d(neighbor_indices, spatial_neighbor_indices)
        for ix in neighbor_indices:
            yield self.ids[ix]

    def delete(self, id_):
        position = self.ids.index(id_)
        del self.ids[position]
        self.values = np.delete(self.values, position, axis=0)
        self.points = np.delete(self.points, position, axis=0)
