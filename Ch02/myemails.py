import pandas as pd

emails = pd.read_csv('data/emails.csv',
                     header=0,
                     names=['emailsOpened', 'member', 'week'],
                     parse_dates=['week'])

print(emails.head())

donations = pd.read_csv('data/donations.csv', parse_dates=['timestamp'])
donations.columns = ['amount', 'timestamp', 'member']

YearJoined = pd.read_csv('data/year_joined.csv')
YearJoined.columns = ['memberId', 'memberStats', 'yearJoined']

complete_idx = pd.MultiIndex.from_product((set(emails.week), set(emails.member)))

all_email = (emails.set_index(['week', 'member'])
                   .reindex(complete_idx, fill_value=0)
                   .reset_index())
all_email.columns = ['week', 'member', 'emailsOpened']

print(all_email[all_email.member==998].sort_values(by='week'))

cutoff_dates = emails.groupby('member').week.agg(['min', 'max']).reset_index()

for _, row in cutoff_dates.iterrows():
    member = row['member']
    start_date = row['min']
    end_date = row['max']
    query = 'member == @member and (week < @start_date or week > @end_date)'
    all_email.drop(all_email.query(query).index, axis='index', inplace=True)

# Constructing a found time series
donations.set_index('timestamp', inplace=True)
agg_don = (donations.groupby('member')
                    .apply(lambda df: df.amount.resample('W-MON').sum()))

agg_don = agg_don[agg_don != 0]
agg_don = agg_don.reset_index().set_index('timestamp')


lst = []
for member, member_email in all_email.groupby('member'):
    member_donations = agg_don.query('member == @member')

    member_email.set_index('week', inplace=True)
    member_email.sort_index(inplace=True)

    df = pd.merge(member_email, member_donations,
                  how='left',
                  left_index=True, right_index=True)
    df.fillna(0, inplace=True)
    df['member'] = df.member_x
    lst.append(df.reset_index()[['member', 'week', 'emailsOpened', 'amount']])

merged_df = pd.concat(lst).set_index('week')
df = merged_df.query('member == 998')     

df['target'] = df.amount.shift(1)
df
