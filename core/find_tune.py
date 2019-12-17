import sys
sys.path.append(".")
import paddlehub as hub
from scripts.datasets import MyDataset 
from settings import BASE_DIR
import os

dataset = MyDataset()
model_path = os.path.join(BASE_DIR, 'resources', 'models', 'express_ner')

def fine_tune(dataset, model_path):
    module = hub.Module(name='ernie')
    reader = hub.reader.SequenceLabelReader(
        dataset=dataset,
        vocab_path=module.get_vocab_path(),
        max_seq_len=128
    )
    
    strategy = hub.AdamWeightDecayStrategy(
        weight_decay=0.01,
        warmup_proportion=0.1,
        learning_rate=5e-5,
        lr_scheduler='linear_decay',
        optimizer_name='adam'
    )
    
    config = hub.RunConfig(
        use_cuda=True,
        num_epoch=10,
        checkpoint_dir=model_path,
        batch_size=16,
        eval_interval=50,
        enable_memory_optim=False,
        strategy=strategy
    )
    
    inputs, outputs, program = module.context(
        trainable=True, max_seq_len=128
    )
    
    sequence_output = outputs['sequence_output']
    
    feed_list = [
        inputs['input_ids'].name,
        inputs['position_ids'].name,
        inputs['segment_ids'].name,
        inputs['input_mask'].name
    ]
    
    seq_label_task = hub.SequenceLabelTask(
        data_reader=reader,
        feature=sequence_output,
        feed_list=feed_list,
        max_seq_len=128,
        num_classes=dataset.num_labels,
        config=config,
        add_crf=True
    )
    
    run_states = seq_label_task.finetune_and_eval()