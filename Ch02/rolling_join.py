import pandas as pd

index = pd.DatetimeIndex(['2019-2-27', '2019-3-2', '2019-6-13',
                          '2019-8-1', '2019-8-31', '2019-9-15'])
data = [99, 100, 5, 15, 11, 1200]
donations = pd.Series(data, index=index)

index = pd.DatetimeIndex(['2019-1-1', '2019-4-1', '2019-7-1'])
data = ['q4q42', '4299hj', 'bbg2']
publicity = pd.Series(data, index=index)
