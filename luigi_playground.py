import luigi
import luigi.contrib.postgres
import luigi.contrib.target
import pandas


class PipelineConfig(luigi.Config):

    host = luigi.Parameter(default='localhost')
    database = luigi.Parameter(default='sales_dw')
    user = luigi.Parameter(default='abhishekzambre')
    password = luigi.Parameter(default='sky')

    customer_info_table = luigi.Parameter(default='customer_info')
    invoice_table = luigi.Parameter(default='invoice')
    product_info_table = luigi.Parameter(default='product_info')


class DataDump(luigi.ExternalTask):
    date = luigi.DateIntervalParameter()

    def run(self):
        print("data/" + str(PipelineConfig.customer_info_table) + ".csv")

    def output(self):
        return [luigi.LocalTarget("data/customer_info.csv"),
                luigi.LocalTarget("data/invoice.csv"),
                luigi.LocalTarget("data/product_info.csv")]


class CustomerInfoCleansing(luigi.Task):
    date_interval = luigi.DateIntervalParameter()

    input_file = "data/customer_info.csv"
    output_file = "temp/customer_info_cleaned.csv"

    def requires(self):
        return DataDump(self.date_interval)

    def run(self):
        data = pandas.read_csv(self.input_file)

        data.country.fillna("Not Available", inplace=True)
        data.country = data.country.str.strip().str.title()
        data.rename(columns={"customerid": "Customer_ID", "country": "Country_Name"}, inplace=True)

        data.to_csv(self.output_file, encoding="utf-8", header=False, index=None)

    def output(self):
        return luigi.LocalTarget(self.output_file)


class InvoiceCleansing(luigi.Task):
    date_interval = luigi.DateIntervalParameter()

    input_file = "data/invoice.csv"
    output_file = "temp/invoice_cleaned.csv"

    def requires(self):
        return DataDump(self.date_interval)

    def run(self):
        data = pandas.read_csv(self.input_file)

        # data.country.fillna("Not Available", inplace=True)
        # data.country = data.country.str.strip().str.title()
        data.rename(columns={"invoiceno": "Invoice_No", "stockcode": "Stock_Code",
                             "invoicedate": "Invoice_Date", "customerid": "Customer_Id"}, inplace=True)

        data.to_csv(self.output_file, encoding="utf-8", header=False, index=None)

    def output(self):
        return luigi.LocalTarget(self.output_file)


class ProductInfoCleansing(luigi.Task):
    date_interval = luigi.DateIntervalParameter()

    input_file = "data/product_info.csv"
    output_file = "temp/product_info_cleaned.csv"

    def requires(self):
        return DataDump(self.date_interval)

    def run(self):
        data = pandas.read_csv(self.input_file)

        # data.country.fillna("Not Available", inplace=True)
        # data.country = data.country.str.strip().str.title()
        data.rename(columns={"stockcode": "Stock_Code", "unitprice": "Unit_Price"}, inplace=True)

        data.to_csv(self.output_file, sep="\t", encoding="utf-8", header=False, index=None)

    def output(self):
        return luigi.LocalTarget(self.output_file)


class CustomerInfoLoading(luigi.contrib.postgres.CopyToTable):
    date_interval = luigi.DateIntervalParameter()

    host = PipelineConfig().host
    database = PipelineConfig().database
    user = PipelineConfig().user
    password = PipelineConfig().password
    table = PipelineConfig().customer_info_table
    column_separator = ","

    columns = [("Customer_ID", "INT"),
               ("Country", "TEXT")]

    def requires(self):
        return CustomerInfoCleansing(self.date_interval)


class InvoiceLoading(luigi.contrib.postgres.CopyToTable):
    date_interval = luigi.DateIntervalParameter()

    host = PipelineConfig().host
    database = PipelineConfig().database
    user = PipelineConfig().user
    password = PipelineConfig().password
    table = PipelineConfig().invoice_table
    column_separator = ","

    columns = [("Invoice_No", "TEXT"),
               ("Stock_Code", "TEXT"),
               ("Quantity", "INT"),
               ("Invoice_Date", "TEXT"),
               ("Customer_Id", "INT")]

    def requires(self):
        return InvoiceCleansing(self.date_interval)


class ProductInfoLoading(luigi.contrib.postgres.CopyToTable):
    date_interval = luigi.DateIntervalParameter()

    host = PipelineConfig().host
    database = PipelineConfig().database
    user = PipelineConfig().user
    password = PipelineConfig().password
    table = PipelineConfig().product_info_table
    column_separator = "\t"

    columns = [("Stock_Code", "TEXT"),
               ("Description", "TEXT"),
               ("Unit_Price", "FLOAT")]

    def requires(self):
        return ProductInfoCleansing(self.date_interval)


class GenerateInsights(luigi.Task):
    date_interval = luigi.DateIntervalParameter()

    def run(self):
        print("Done.")

    def requires(self):
        return [CustomerInfoLoading(self.date_interval),
                InvoiceLoading(self.date_interval),
                ProductInfoLoading(self.date_interval)]
