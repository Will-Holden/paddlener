from core.base.data.lshash import LSHash
import numpy as np


class LSHBasedFixSizeHash:
    def __init__(self, max_length=10000, hash_size=128, input_dim=128):
        self.max_length = max_length
        self.lsh = LSHash(hash_size, input_dim, max_length=max_length, num_hashtables=128)

    def add(self, item):
        self.lsh.index(item.digest())

    def get_max_similar(self, item):
        candidate = self.lsh.query(item.digest(), distance_func="cosine", num_results=50)
        return max([self.jaccard(item.digest(), data[0]) for data in candidate]) if candidate else 0

    @classmethod
    def jaccard(cls, item1, item2):
        return np.float(np.count_nonzero(np.array(item1) == np.array(item2))) / np.float(len(item1))


if __name__ == '__main__':
    lsh = LSHash(128, 8, num_hashtables=128)
    lsh.index([1, 2, 3, 4, 5, 6, 7, 8])
    lsh.index([2, 3, 4, 5, 6, 7, 8, 9])
    lsh.index([10, 12, 99, 1, 5, 31, 2, 3])
    print(lsh.query([1, 2, 3, 4, 5, 6, 7, 7], num_results=2, distance_func="cosine"))
    print(LSHBasedFixSizeHash.jaccard([1, 2, 3], [1, 2, 4]))
