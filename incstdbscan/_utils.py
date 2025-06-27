import xxhash
from sklearn.utils.validation import check_array


def hash_(array):
    return xxhash.xxh64_intdigest(array.tobytes()) >> 1


def input_check(X,points):
    return check_array(X, dtype=float, accept_large_sparse=False),check_array(points, dtype=float, accept_large_sparse=False)
