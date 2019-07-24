import pandas as pd
import heapq


class FixSizeDataFrame:
    def __init__(self, data, sort_by='PubTime', **kwargs):
        self.value = pd.DataFrame(data)
        self.index_heap = []
        self.sort_by = sort_by
        self.construct_head()
        self.max_length = -1
        self.min_value = -1
        if 'max_length' in kwargs.keys():
            self.max_length = kwargs['max_length']
        elif 'min_value' in kwargs.keys():
            self.min_value = kwargs['min_value']

    def construct_head(self):
        for index, item in self.value.iterrows():
            heap_item = (item[self.sort_by], index)
            heapq.heappush(self.index_heap, heap_item)

    def push_data(self, item):
        if self.value.last_valid_index() is None:
            index = 0
            self.value = pd.DataFrame(columns=list(item.keys()))
            # self.value.set_index('index')
        else:
            index = self.value.last_valid_index() + 1
        item['index'] = index
        heap_item = (item[self.sort_by], index)
        heapq.heappush(self.index_heap, heap_item)
        self.value.loc[index] = item
        self.fresh_heap()

    def fresh_heap(self):
        """

        :return:
        """

        if self.min_value == -1 and self.max_length == -1:
            print("no min_alue none max_length setted")
        # 如果设定最小值，则按照最小值调整
        if self.min_value != -1:
            heap_item = heapq.heappop(self.index_heap)
            while heap_item[1] < self.min_value:
                self.value.drop(index=heap_item[0])
                heap_item = heapq.heappop(self.index_heap)
            heapq.heappush(self.index_heap, heap_item)

        # 如果设定最大长度，则按照最大长度调整
        if self.max_length != -1:
            while len(self.index_heap) > self.max_length:
                heap_item = heapq.heappop(self.index_heap)
                self.value = self.value.drop(index=heap_item[1])
                # self.value

    def pop_data(self):
        heap_item = heapq.heappop(self.index_heap)
        result = self.value.loc[heap_item[1]]
        self.value.drop(heap_item[1])
        return result
