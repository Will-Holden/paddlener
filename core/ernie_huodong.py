import sys
sys.path.append(".")
import numpy as np 
from scripts.datasets import MyDataset 
from settings import BASE_DIR
import paddlehub as hub
import copy
import os

labels = [
    "B-ZZ", 'I-ZZ', "B-D", 'I-D', "B-S", 'I-S', "B-ZW", 'I-ZW', "B-RW", 'I-RW', "B-HD", 'I-HD', "B-JG", 'I-JG', "O"
]

data_path = os.path.join(BASE_DIR, 'resources', 'datasets', 'huodong')
dataset = MyDataset(dataset_dir=data_path, labels=labels)

model_path = os.path.join(BASE_DIR, 'resources', 'models', 'huodong')

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


def huodong_ner(text):
    data = [text[i: i+ 125] for i in range(0, len(text), 125)]
    data = [[x] for x in data]
    data = [["\x02".join(list(x[0])).replace("\x02 \x02", "\x02\x02-\x02")] for x in data]
    # data = [['\002'.join(list(x[0]))] for x in data]

    run_states = seq_label_task.predict(data=data)
    results = [run_state.run_results for run_state in run_states]
    # data = [[x[0].replace("\002",'')] for x in data]
    data = [[x[0].replace("\x02\x02-\x02", "\x02 \x02").replace('\x02', "")] for x in data]

    data_labels = copy.deepcopy(data)
    for num_batch, batch_results in enumerate(results):
        infers = batch_results[0].reshape([-1]).astype(np.int32).tolist()
        np_lens = batch_results[1]

        cut = 0
        for index, np_len in enumerate(np_lens):
            # labels = infers[index*128: (index +1) * 128]
            labels = infers[cut:cut + np_len]
            cut = cut+np_len

            label_strs = []
            count = 0
            for label_val in labels:
                label_strs.append(inv_label_map[label_val])
                count += 1
                if count == np_len:
                    break
            
            data_labels[num_batch + index][0] = label_strs[1:-1]
    return [tag for label in data_labels for tag in label[0]]

if __name__ == "__main__":
    datas = """2019年8月29日，备受业界关注的“2019世界人工智能大会”在上海拉开帷幕。比尔·盖茨曾说“语言理解是人工智能皇冠上的明珠
。自然语言处理的进步将会推动人工智能整体进展。”8月30日，由达观数据和乐言科技联合主办的《理解语言，拥抱智能》主题论坛在上海世博中心重磅开启。
　　长宁区委常委、副区长、区政府党组副书记钟晓敏，浦东新区副区长管小军，国际计算语言学(ACL)终身成就奖得主、中国中文信息学会名誉理事长李生
教授出席本次活动，论坛同时还邀请到伊利诺伊大学香槟分校教授Heng Ji，苏州大学特聘教授、国家杰出青年科学基金获得者张民，复旦大学教授、中国中文信息学会常务理事黄萱菁，中国人工智能学会常务理事、北京邮电大学教授王小捷、达观数据CEO陈运文和乐言科技CEO沈李斌多位世界级AI领袖，与现场来宾分享人工智能发展的独到深刻观点。本次论坛从自然语言处理出发，围绕语言智能的学术与应用展开了最前沿和务实的讨论。
　　达观数据创始人陈运文博士以《具备语义智能理解的RPA流程机器人》为题，分享了自然语言处理技术目前在工业界的应用，他谈到“文字的自动化处理面临一个非常好的机遇。深度神经网络的技术从2006年由Hinton教授提出来以后，经过十多年的发展越来越来成熟，尤其是用在文本智能处理领域。他介绍通过将NLP技术与机器人流程自动化(RPA)结合，可以赋予机器人阅读思考的能力，在现有各类工作系统中协助完成阅读撰写等流程性的重复工作。目前达观数据在商业案例报告生成、智慧政务行政审批、金融文档验查和填写等场景中，推出的机器人员工已逐步开展各项工作。”
　　乐言科技创始人沈李斌博士以《认知智能赋能企业计算》为题，分享了以自然语言处理、知识图谱、机器学习为核心的认知智能技术在企业计算中的广泛应用。
　　在大会期间，世界人工智能大会WAIC联合达观数据联合推出了AI新闻助手，该助手集成自然语言处理(NLP)与光学字符识别(OCR)技术，让文字工作者们在文章素材采集转写、自动摘要撰写、内容分类等方面体验人工智能的便捷。
　　该助手还可快速做出符合规范的五言、七言绝句，绝句灵活轻便，声调平仄相对。据达观数据创始人陈运文介绍，新闻助手对五万余首全唐诗进行了“语料”学习，通过生成语义分析模型，并经过不断训练后，最终具备“出口成章”的能力。
　前不久，达观数据发布了国内首款自主研发集 NLP(自然语言处理)与OCR(光学字符识别)于一体的达观智能RPA。通过让让计算机学习和模仿人类处理任务的步骤，协助完成重复性的文书操作工作，为企业打造智能数字化员工。
　　语言作为人类交流的重要方式，人工智能将如何破译人类语言的密码?在智能化技术的发展过程中，自然语言处理技术助推各行业催生的新产品为生产力带来了质的飞跃。
　　语言智能作为人工智能发展中的核心 ，将改变我们在工作中对文档内容的阅读、审阅和生产方式。随着自然语言处理技术的发展和应用，人机协作的未来有很大想象空间。"""
    datas = datas.replace('\n','').replace('\u3000', '').replace('\n', '')
    labels = huodong_ner(datas)
    print(labels)
    # print(len(labels))
    # print(len(datas))
    # labels = huodong_ner(datas)