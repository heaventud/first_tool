#!/usr/bin/env python3

import pandas as pd
import numpy as np
from jinja2 import Template
from pandas.io.formats.style import Styler

np.random.seed(24)
df = pd.DataFrame({'A': np.linspace(1, 10, 10)})
df = pd.concat([df, pd.DataFrame(np.random.randn(10, 4), columns=list('BCDE'))],
               axis=1)
df.iloc[3, 3] = np.nan
df.iloc[0, 2] = np.nan


EasyStyler = Styler.from_custom_template("", "view.html")

with open('epic.html', 'w') as fd:
    fd.write(EasyStyler(df).render(table_title="Extending Example"))
