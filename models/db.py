db = DAL('sqlite://storage.sqlite')
db.define_table('sales',Field('Transaction_date'),Field('Product'),Field('Price'),Field('Payment_Type'),Field('Country'))
db.define_table('gdp',Field('CountryName'),Field('CountryCode'),Field('Year'),Field('Gdp'))

