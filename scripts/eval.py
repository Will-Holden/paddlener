import sys
sys.path.append(".")
import numpy as np 
from scripts.datasets import MyDataset 
from settings import BASE_DIR
import paddlehub as hub
import os

dataset = MyDataset()
model_path = os.path.join(BASE_DIR, 'resources', 'models', 'express_ner')
# data = [
#         ["\002".join(list(u"喻晓刚云南省楚雄彝族自治州南华县东街古城路37号18513386163"))],
#         ["\002".join(list(u"河北省唐山市玉田县无终大街159号18614253058尚汉生"))],
#         ["\002".join(list(u"台湾嘉义县番路乡番路乡公田村龙头17之19号宣树毅13720072123"))],
#     ]


def myeval(dataset, model_path, datas):
    module = hub.Module(name="ernie")
    inputs, outputs, program = module.context(max_seq_len=128)
    
    # Sentence labeling dataset reader
    reader = hub.reader.SequenceLabelReader(
        dataset=dataset,
        vocab_path=module.get_vocab_path(),
        max_seq_len=128
        )
    
    sequence_output = outputs["sequence_output"]
    
    strategy = hub.AdamWeightDecayStrategy(
        weight_decay=0.01,
        warmup_proportion=0.1,
        learning_rate=5e-5,
        lr_scheduler="linear_decay")
    
    
    config = hub.RunConfig(
        use_cuda=True,
        num_epoch=1,
        checkpoint_dir= model_path,
        batch_size=16,
        eval_interval=50,
        enable_memory_optim=False,
        strategy=strategy)
    
    feed_list = [
        inputs["input_ids"].name,
        inputs["position_ids"].name,
        inputs["segment_ids"].name,
        inputs["input_mask"].name,
    ]
    
    seq_label_task = hub.SequenceLabelTask(
        data_reader=reader,
        feature=sequence_output,
        feed_list=feed_list,
        add_crf=True,
        max_seq_len=128,
        num_classes=dataset.num_labels,
        config=config)
    
    inv_label_map = {val: key for key, val in reader.label_map.items()}
    
    
    run_states = seq_label_task.predict(data=datas)
    results = [run_state.run_results for run_state in run_states]

    datas = [
        [x[0].replace('\002', '')] for x in datas
    ]
    
    for num_batch, batch_results in enumerate(results):
        infers = batch_results[0].reshape([-1]).astype(np.int32).tolist()
        np_lens = batch_results[1]

        cuts = 0
        for index, np_len in enumerate(np_lens):
            labels = infers[cuts:cuts+ np_len]
            cuts = cuts + np_len

            label_str = []
            count = 0
            for label_val in labels:
                label_str.append(inv_label_map[label_val])
                count += 1
                if count == np_len:
                    break

            huodongs = []
            tmp_ent = []
            class_label = ""

            for word, label in zip(list(datas[num_batch + index][0]), list(label_str[1:-1])):
                if label == 'B-HD':
                    class_label = 'huodong'
                    tmp_ent.append(word)
                elif label == 'I-HD' and class_label == '':
                    class_label = 'huodong'
                    tmp_ent.append(word)
                elif label == 'I-HD':
                    tmp_ent.append(word)
                elif label == 'O' and class_label == 'huodong':
                    class_label = ""
                    huodongs.append(tmp_ent)
                    tmp_ent = []


            print(datas[num_batch + index][0])
            print(label_str[1:-1])
            print('label lens:', np_len)
            print('data lens', len(datas[num_batch + index][0]))
            print('huodong: \n' + ",".join([''.join(x) for x in huodongs]))