from typing import Dict

from ._labels import LabelHandler
from ._neighbor_searcher import NeighborSearcher
from ._object import (
    Object,
    ObjectId
)
from ._utils import hash_
import numpy as np

class Objects(LabelHandler):
    def __init__(self, eps,spatial_eps, metric, p):
        super().__init__()
        self.objects: Dict[ObjectId, Object] = {}
        self.neighbor_searcher = \
            NeighborSearcher(radius=eps,spatial_radius=spatial_eps, metric=metric, p=p)

    def get_object(self, value,point):
        id_ = hash_(np.append([value],[point], axis=1))
        return self.objects.get(id_)

    def insert_object(self, value, point):
        id_ = hash_(np.append([value],[point], axis=1))

        if id_ in self.objects:
            obj = self.objects[id_]
            obj.count += 1
            return obj

        new_object = Object(id_)
        self.objects[id_] = new_object
        self.set_label_of_inserted_object(new_object)

        self.neighbor_searcher.insert(value, point, id_)
        self._update_neighbors_during_insertion(new_object, value, point)
        return new_object

    def _update_neighbors_during_insertion(self, object_inserted, new_value, new_point):
        neighbors = self._get_neighbors(new_value, new_point)
        for obj in neighbors:
            obj.neighbors.add(object_inserted)
            object_inserted.neighbors.add(obj)

    def _get_neighbors(self, query_value, query_point):
        neighbor_ids = self.neighbor_searcher.query_neighbors(query_value, query_point)

        for id_ in neighbor_ids:
            yield self.objects[id_]

    def delete_object(self, obj):
        obj.count -= 1
        if obj.count == 0:
            del self.objects[obj.id]
            self.neighbor_searcher.delete(obj.id)
            self._update_neighbors_during_deletion(obj)
            self.delete_label_of_deleted_object(obj)

    @staticmethod
    def _update_neighbors_during_deletion(object_deleted):
        effective_neighbors = \
            object_deleted.neighbors.difference({object_deleted})
        for neighbor in effective_neighbors:
            neighbor.neighbors.remove(object_deleted)
