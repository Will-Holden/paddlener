import os
import codecs
import csv

from paddlehub.dataset import InputExample, HubDataset
from settings import BASE_DIR


class MyDataset(HubDataset):
    """
    A set of manually Chinese word-segmentation data about experess information extraction.
    """

    def __init__(self, dataset_dir=os.path.join(BASE_DIR, "resources", 'datasets', 'express_ner'), labels=[
            "B-P", "I-P", "B-T", "I-T", "B-A1", "I-A1", "B-A2", "I-A2", "B-A3",
            "I-A3", "B-A4", "I-A4", "O"
        ]):
        self.dataset_dir = dataset_dir
        self.labels = labels
        self._load_train_examples()
        self._load_test_examples()
        self._load_dev_examples()

    def _load_train_examples(self):
        train_file = os.path.join(self.dataset_dir, "train.txt")
        self.train_examples = self._read_file(train_file)

    def _load_dev_examples(self):
        self.dev_file = os.path.join(self.dataset_dir, "dev.txt")
        self.dev_examples = self._read_file(self.dev_file)

    def _load_test_examples(self):
        self.test_file = os.path.join(self.dataset_dir, "test.txt")
        self.test_examples = self._read_file(self.test_file)

    def get_train_examples(self):
        return self.train_examples

    def get_dev_examples(self):
        return self.dev_examples

    def get_test_examples(self):
        return self.test_examples

    def get_labels(self):
        return self.labels

    @property
    def num_labels(self):
        """
        Return the number of labels in the dataset.
        """
        return len(self.get_labels())

    def _read_file(self, input_file, quotechar=None):
        """Reads a tab separated value file."""
        with codecs.open(input_file, "r", encoding="UTF-8") as f:
            reader = csv.reader(f, delimiter="\t", quotechar=quotechar)
            examples = []
            seq_id = 0
            # 跳过表头
            header = next(reader)  # skip header
            for line in reader:
                example = InputExample(
                    guid=seq_id, label=line[1], text_a=line[0])
                seq_id += 1
                examples.append(example)

            return examples

if __name__ == "__main__":
    dataset = MyDataset()
    count = 0
    sum_len = 0
    for e in dataset.get_train_examples():
        count += 1
        sum_len += len(e.text_a)
        if count<3:
            print("{}\t{}\t{}".format(e.guid, e.text_a, e.label))