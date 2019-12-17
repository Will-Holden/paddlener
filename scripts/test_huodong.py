from scripts.find_tune import fine_tune
from scripts.eval import myeval
from scripts.datasets import MyDataset
from settings import BASE_DIR
import os

labels = [
    "B-ZZ", 'I-ZZ', "B-D", 'I-D', "B-S", 'I-S', "B-ZW", 'I-ZW', "B-RW", 'I-RW', "B-HD", 'I-HD', "B-JG", 'I-JG', "O"
]

data_path = os.path.join(BASE_DIR, 'resources', 'datasets', 'huodong')
dataset = MyDataset(dataset_dir=data_path, labels=labels)

model_path = os.path.join(BASE_DIR, 'resources', 'models', 'huodong')
# fine_tune(dataset, model_path)

data = [
        ["\002".join(list(u"在第六届世界互联网大会上，百度创始人李彦宏在开幕式上进行了主题演讲。"))],
        ["\002".join(list(u"作为在金融领域成熟落地的AI企业，快商通携“声纹反欺诈风控系统”亮相本届WAIC。"))],
        ['\002'.join(list(u'2019年8月29日，备受业界关注的“2019世界人工智能大会”在上海拉开帷幕。'))],
        ['\002'.join(list(u'由西安交通大学软件学院和深圳市云积分科技有限公司（简称“云积互动”）联合举办的“2019数据智能算法大赛”全国六强历经四个月的重重冲关，今日终于尘埃落定。'))]
]

myeval(dataset, model_path, data)