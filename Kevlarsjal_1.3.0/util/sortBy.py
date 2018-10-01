def sort_by_sector(df,name):
    return df[(df['Sector'] == name)]

def sort_by_industry(df,name):
    return df[(df['Industry'] == name)]
