# -*- coding: utf-8 -*-

import pandas as pd
import os
from ddf_utils.str import to_concept_id
from ddf_utils.index import create_index_file


# configuration of file paths
source = '../source/gapdata010.xls'
out_dir = '../../'


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
    dps = dps.set_index(['country', 'year'])

    for i, df in dps.items():
        path = os.path.join(out_dir, 'ddf--datapoints--{}--by--country--year.csv'.format(i))
        df_ = df.reset_index()
        df_.sort_values(by=['country', 'year'])\
           .dropna()\
           .to_csv(path, index=False)

    create_index_file(out_dir)

    print('Done.')
