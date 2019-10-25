import pandas as pd

YearJoined = pd.read_csv('data/year_joined.csv')
emails = pd.read_csv('data/emails.csv', parse_dates=['week'])
print((max(emails[emails.user == 998].week) - min(emails[emails.user == 998].week)).days / 7)
complete_idx = pd.MultiIndex.from_product((set(emails.week), set(emails.user)))
all_emails = emails.set_index(['week', 'user']).reindex(complete_idx, fill_value=0).reset_index()
all_emails.columns = ['week', 'member', 'EmailsOpened']
all_emails
all_emails[all_emails.member == 998].sort_values('week')
cutoff_dates = emails.groupby('user').week.agg(['min', 'max']).reset_index()
cutoff_dates.columns = ['member', 'min', 'max']

print("Drop rows from the dataframe that don't contribute sensibly to the chronology")
for _, row in cutoff_dates.iterrows():
    member = row['member']
    start_date = row['min']
    stop_date = row['max']

    idx = all_emails.query('member == @member & (week < @start_date | week > @stop_date)').index
    all_emails.drop(index=idx, inplace=True)

print(len(all_emails))

all_email = all_emails

print('Constructing a found time series')
donations = pd.read_csv('data/donations.csv', parse_dates=[1], index_col='timestamp')
donations.columns = ['amount', 'member']

fcn = lambda df: df.amount.resample('W-MON').sum()
agg_don = donations.groupby('member').apply(fcn).reset_index().query('amount > 0')


print('Merge the dataframes')
lst = []
for member, member_email in all_email.groupby('member'):
    member_donations = agg_don[agg_don.member == member]
    member_donations.set_index('timestamp', inplace=True)
    member_email.set_index('week', inplace=True)

    df = pd.merge(member_email, member_donations, how='left', left_index=True, right_index=True)
    df.fillna(0, inplace=True)
    df['member'] = df.member_x

    lst.append(df.reset_index()[['member', 'week', 'EmailsOpened', 'amount']])
merged_df = pd.concat(lst).sort_values(by=['member', 'week'])

df = merged_df[merged_df.member == 998]
df['target'] = df.amount.shift(1)
df.fillna(0)
