import pandas as pd
import numpy as np
import re
import os

# scanデータの成型
input_path = '/home/togawa/data/messenger/fips/cdr/scan'
output_path = '/data/togawa/messenger/fips/cdr/scan'
EQTAB = [ 0.0464,  0.0511,  0.0564,  0.062 ,  0.0683,  0.0754, 0.0829,
         0.0913,  0.1004,  0.1107,  0.1219,  0.134 ,  0.1478, 0.1627,
         0.1789,  0.197 ,  0.217 ,  0.2388,  0.2631,  0.2896, 0.3189,
         0.351 ,  0.3863,  0.4255,  0.4682,  0.5156,  0.5677, 0.6251,
         0.688 ,  0.7576,  0.8343,  0.9184,  1.011 ,  1.1133, 1.2255,
         1.3493,  1.4855,  1.6358,  1.8007,  1.9828,  2.183 , 2.4034,
         2.6459,  2.9131,  3.2074,  3.531 ,  3.8877,  4.2802, 4.7126,
         5.1884,  5.7121,  6.2892,  6.9243,  7.6233,  8.393 , 9.2407,
        10.1738, 11.2011, 12.3322, 13.5774, 14.9482, 16.4578, 18.1198,
        19.9492]  
EQTAB.reverse()
files_file = [
    f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))
]

count = 0
for file in files_file:
    count += 1
    print(file)
    print(str(count)+'/'+str(len(files_file)))
    if os.path.isfile(output_path + '/' + file):
        continue
    tmp = pd.read_pickle(input_path + '/' + file)
    result = pd.DataFrame()
    date = []
    for i in tmp[1].values:
        m = re.match(r'(\d{4})-(\d{3})T(\d{2}):(\d{2}):(\d{2}).(.*)',i)
        year = int(m.group(1))
        day = int(m.group(2))
        hour = int(m.group(3))
        minute = int(m.group(4))
        second = int(m.group(5))
        msecond = int(m.group(6))
        a = pd.Timedelta(days=day-1, hours=hour, minutes=minute, seconds=second, milliseconds=msecond)
        date.append(pd.to_datetime(year*1000 + 1, format='%Y%j') + a)
    for i in range(5):
        for j in range(len(EQTAB)):
            result[EQTAB[j]] = tmp.values[:,4+j+i*len(EQTAB)]
    result['date'] = date
    result = result.set_index('date')
    result.to_pickle(output_path + '/' + file)