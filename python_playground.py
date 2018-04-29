import pandas as pd

data = pd.read_csv("data/product_info.csv")

cols = data.columns.tolist()

cols = [cols[0]] + [cols[2]] + [cols[1]]

data = data[cols]

print(data)


#print(data.invoiceno.describe())

# data.country.fillna("Not Available", inplace=True)
# data.country = data.country.str.strip().str.title()
# data.rename(columns={"customerid": "Customer_ID", "country": "Country"}, inplace=True)
# print(data)

