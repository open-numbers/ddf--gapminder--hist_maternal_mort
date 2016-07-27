# -*- coding: utf-8 -*-

import pandas as pd
import os
from ddf_utils.str import to_concept_id
from ddf_utils.index import create_index_file


# configuration of file paths
source = '../source/gapdata010.xls'
out_dir = '../../'


def fix_time_range(s):
    """change a time range to the middle of year in the range.
    e.g. fix_time_range('1980-90') = 1985
    """

    if '-' not in s:
        return int(s)

    else:
        t1, t2 = s.split('-')
        if len(t1) == 4 and len(t2) == 4:
            span = int(t2) - int(t1)
            return int(int(t1) + span / 2)
        else:  # t2 have only 1-2 digits.
            d = len(t2)
            hund1 = int(t1[:4-d])
            tens1 = int(t1[-d:])
            tens2 = int(t2)
            y1 = int(t1)
            if tens1 > tens2:
                hund2 = hund1 + 1
                y2 = hund2 * 10**d + tens2
            else:
                y2 = hund1 * 10**d + tens2

            return int(y1 + (y2 - y1) / 2 )

if __name__ == '__main__':
    data = pd.read_excel(source, na_values=['..', '...', 'no data'])
    data = data.set_index('Country')
    data = data.dropna(how='all')
    data = data.reset_index()

    # entities
    country = data[['Country']].copy()
    country['country'] = country['Country'].map(to_concept_id)
    country.columns = ['name', 'country']
    country = country.drop_duplicates()
    path = os.path.join(out_dir, 'ddf--entities--country.csv')
    country.to_csv(path, index=False)

    # concepts
    conc = ['MMR', 'Live Births', 'Maternal deaths',
            'Women reproductive age (15-49)', 'MM-rate']
    conc_id = list(map(to_concept_id, conc))
    cdf = pd.DataFrame([], columns=['concept', 'name', 'concept_type'])

    cdf['name'] = conc
    cdf['concept'] = conc_id
    cdf['concept_type'] = 'measure'

    desc = pd.DataFrame([['name', 'Name', 'string'],
                         ['year', 'Year', 'string'],
                         ['country', 'Country', 'entity_domain']], columns=cdf.columns)
    call = pd.concat([desc, cdf])

    path = os.path.join(out_dir, 'ddf--concepts.csv')
    call.to_csv(path, index=False)

    # datapoints
    dps_cols = ['Country', 'year', *conc]
    dps = data[dps_cols].copy()
    dps.columns = list(map(to_concept_id, dps.columns))
    dps['country'] = dps['country'].map(to_concept_id)

    # fix the year range problem
    dps['year'] = dps['year'].map(lambda x: fix_time_range(str(x)))

    dps = dps.set_index(['country', 'year'])

    for i, df in dps.items():
        path = os.path.join(out_dir, 'ddf--datapoints--{}--by--country--year.csv'.format(i))
        df_ = df.reset_index()
        df_.sort_values(by=['country', 'year'])\
           .dropna()\
           .to_csv(path, index=False)

    create_index_file(out_dir)

    print('Done.')
