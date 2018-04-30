import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import apriori
from ast import literal_eval
import csv

data = pd.read_csv("orig_data/invoice.csv")

grouped = data[['customerid', 'stockcode']].groupby('customerid')

# data2 = grouped.aggregate(lambda x: ','.join(x))
data2 = grouped.aggregate(lambda x: list(x))


data2.to_csv("test.csv", encoding="utf-8", header=False, index=None)

temp = list()
with open("test.csv", 'r') as f:
    for row in csv.reader(f):
        eval_temp = literal_eval(''.join(row))
        if len(eval_temp) == 1:
            continue
        temp.append(eval_temp)

te = TransactionEncoder()
te_ary = te.fit(temp).transform(temp)
df = pd.DataFrame(te_ary, columns=te.columns_)
frequent_itemsets = apriori(df, min_support=0.05, use_colnames=True)
association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)

final_rules = pd.DataFrame([rules['antecedants'].str.join(''),
                            rules['consequents'].str.join(''),
                            rules['antecedent support'],
                            rules['consequent support'],
                            rules['support'],
                            rules['confidence'],
                            rules['lift'],
                            rules['leverage'],
                            rules['conviction']]).T

final_rules.to_csv("output.csv", encoding="utf-8", header=False, index=None)