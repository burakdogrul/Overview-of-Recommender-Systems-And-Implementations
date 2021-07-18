!pip install openpyxl
!pip install mlxtend

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)

dataframe = pd.read_excel("C:/Users/Burak/Recommendation_Systems/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = dataframe.copy()

def check_df(dataframe):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(3))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.describe().T)

def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

def retail_data_prep(dataframe):
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
    return dataframe

check_df(df)

df = retail_data_prep(df)

check_df(df)


df_ger = df[df['Country'] == "Germany"]
check_df(df_ger)

stockpost = df_ger[df_ger["StockCode"] == "POST"].index
descpost = df_ger[df_ger["Description"] == "POSTAGE"].index
df_ger = df_ger[~df_ger.index.isin(stockpost)]
df_ger = df_ger[~df_ger.index.isin(descpost)]


def create_invoice_product_df(dataframe, id=True):
    if id:
        return dataframe.groupby(['Invoice', "StockCode"])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)
    else:
        return dataframe.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)

ger_inv_pro_df = create_invoice_product_df(df_ger)
ger_inv_pro_df.head()

frequent_itemsets = apriori(ger_inv_pro_df, min_support=0.01, use_colnames=True)
frequent_itemsets.sort_values("support", ascending=False)

rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)
rules.sort_values("lift", ascending=False)


def check_id(dataframe, stock_code):
    product_name = dataframe[dataframe["StockCode"] == stock_code][["Description"]].values[0].tolist()
    return product_name


def arl_recommender(rules_df, product_id, rec_count=1, productname=False):
    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_list = []
    unique_recommendation_list = []
    productname_list = []
    for i, product in enumerate(sorted_rules["antecedents"]):
        for j in list(product):
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])
    for k in recommendation_list:
        if k not in unique_recommendation_list:
            unique_recommendation_list.append(k)
    if productname:
        for m in unique_recommendation_list:
            productname_list.append(check_id(df_ger, m)[0])
        return productname_list[0:rec_count]
    else:
        return unique_recommendation_list[0:rec_count]


# RECOMMEND-1
arl_recommender(rules, 21987, 3, productname=True)

#RECOMMEND-2
arl_recommender(rules,23235,3, productname=True)

#RECOMMEND-3
arl_recommender(rules,22747,3, productname=True)

