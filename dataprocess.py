import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def analyse(file, font_prop):
    data = pd.read_csv(file)
    cn_webnums = 0
    lenth = len(data['md5_domain'])
    
    for n in data['爬虫网页数量']:
        if n < 3:
            cn_webnums += 1
    
    valid_web = data[data['爬虫网页数量'] < 3]
    companys = data[data["company_name"].notna()]
    duplicated_com = companys["company_name"].duplicated(keep='first').sum()
    md5 = data[data["md5_domain"].notna()]
    duplicated_md5 = md5["md5_domain"].duplicated(keep='first').sum()
    empty_md5 = data[data["md5_domain"].isna()]
    num_empty_md5 = data["md5_domain"].isna().sum()
    empty_company = data["company_name"].isna().sum()
    empty_profile = data["企业简介"].isna().sum()
    empty_products = data["公司产品"].isna().sum()
    profile_product = data[(data["企业简介"].notna()) | (data["公司产品"].notna())]
    pp_rows = profile_product.shape[0]
    
    # 检查无效网页与空值行是否存在重叠
    valid_web_set = set(valid_web.index.tolist())
    empty_md5_set = set(empty_md5.index.tolist())
    if len(valid_web_set.intersection(empty_md5_set)) == 0:
        print("不存在重叠")
    else:
        print("空值行数与无效网页的重叠条数为:",len(valid_web_set.intersection(empty_md5_set)))
    overlap1 = len(valid_web_set.intersection(empty_md5_set))

    # 检查无效网页与包含公司名称行的重叠情况
    companys_set = set(companys.index.tolist())
    if len(valid_web_set.intersection(companys_set)) == 0:
        print("不存在重叠")
    else:
        print("无效网页中包含公司信息的有:",len(valid_web_set.intersection(companys_set)))
    overlap2 = len(valid_web_set.intersection(companys_set))
    valid_set_company = valid_web_set.intersection(companys_set)

    # 检查无效网页中包含公司信息部分中含有有价值信息的部分
    pp_set = set(profile_product.index.tolist())
    if len(pp_set.intersection(valid_set_company)) == 0:
        print("不存在重叠")
    else:
        print("无效网页中包含公司信息的有:",len(pp_set.intersection(valid_set_company)))
    overlap3 = len(pp_set.intersection(valid_set_company))

    print("信息条数:", lenth)
    print("列信息:")
    print(data.columns)
    print("无效网页数量(网页数量<3):", cn_webnums)
    print("空值行数:", num_empty_md5)
    print("顺利抽取到的公司条数:", lenth - empty_company)
    print("不包含公司简介的条数:", empty_profile - empty_company)
    print("不包含公司产品的条数:", empty_products - empty_company)
    print("具有简介或产品的条数:", pp_rows)
    print("重复公司名称的条数:", duplicated_com)
    print("重复MD5标识的条数:", duplicated_md5)

    valid_vs_all = round(7/6, 2)

    pie_series = []
    va_se = []
    web_se = []
    vr_se = []

    valid_labels = ['包含有效公司信息', '包含无效公司信息','空值']
    web_labels = ['空值', '包含有效信息', '信息无效']
    all_labels = ['空值','有效公司信息','无效公司信息']
    va_rate = ['无效网页','有效网页']
    vrcolors = ['purple', 'pink']

    vcolors = ['blue','green','red']
    wcolors = ['purple', 'pink','orange']

    pie_series.append(num_empty_md5)
    pie_series.append(pp_rows)
    pie_series.append(lenth - empty_company - pp_rows)

    va_se.append(overlap3)
    va_se.append(cn_webnums - overlap3 - num_empty_md5)
    va_se.append(overlap1)

    web_se.append(num_empty_md5 - overlap1)
    web_se.append(pp_rows)
    web_se.append(lenth - empty_company - pp_rows)

    vr_se.append(cn_webnums)
    vr_se.append(lenth - cn_webnums)
    # 设置中文字体格式
    plt.rcParams['font.sans-serif'] = font_prop.get_name()
    plt.rcParams["axes.unicode_minus"]=False

    plt.pie(va_se, labels=web_labels, colors=wcolors, autopct='%0.1f%%')
    plt.axis('equal')
    plt.title('有效网页结果分析')
    plt.savefig('/home/daixingshuo/dataprocess/web_pie.png')

    plt.clf()
    plt.pie(web_se, labels=valid_labels, colors=vcolors, autopct='%0.1f%%')
    plt.axis('equal')
    plt.title('无效网页结果分析')
    plt.savefig('/home/daixingshuo/dataprocess/valid_pie.png')

    plt.clf()
    plt.pie(va_se, labels=all_labels, colors=vcolors, autopct='%0.1f%%')
    plt.axis('equal')
    plt.title('总体结果分析')
    plt.savefig('/home/daixingshuo/dataprocess/all_pie.png')

    plt.clf()
    plt.pie(vr_se, labels=va_rate, colors=vrcolors, autopct='%0.1f%%')
    plt.axis('equal')
    plt.title('无效网页占比')
    plt.savefig('/home/daixingshuo/dataprocess/valid_rate_pie.png')

if __name__ == "__main__":
    file_path = "/home/songxianxin/gitlab/uie/inference_8w_zjtx/8.29数据统计.csv"
    font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    font_prop = FontProperties(fname=font_path)
    analyse(file_path, font_prop)