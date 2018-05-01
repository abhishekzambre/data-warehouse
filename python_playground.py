import numpy
import pandas


data = pandas.read_csv("orig_data/invoice.csv")
quantity = data['quantity']

q75, q25 = numpy.percentile(quantity, [75, 25])

iqr = q75 - q25

upper_fence = q75 + (30.0 * iqr)

outliers = data[data.quantity > upper_fence]

print(outliers)