import itertools
from functools import partial
import pandas as pd
import os
import webbrowser
import numpy as np
from configparser import ConfigParser
from pandas.io.formats.style import Styler


def get_stats(array):
    return array.mean(), array.median(), array.quantile(.95)


def color_red(val):
    if not np.isnan(val):
        color = 'red' if val > 0.2 else 'black'
        return 'color: {%s}' % color
    return val


def format_percents(val):
    if not np.isnan(val):
        return "{:.2} %".format(val)


STAT_FUNC = {
    'average':
        np.mean,
    'median':
        np.median,
    'p95':
        partial(np.quantile, q=.95)
}


def run(filename1, filename2):
    """
    """
    table1 = pd.read_csv(filename1)
    table2 = pd.read_csv(filename2)
    table1.columns = table1.columns.str.replace("\\", "_")\
        .str.replace("^__", "", regex=True)\
        .str.replace('%', '')
    table2.columns = table2.columns.str.replace("\\", "_").str.replace("^__", "", regex=True) \
        .str.replace('%', '')
    stats = {}
    for idx, column in enumerate(table1.columns[1:]):
        table1[column] = pd.to_numeric(table1[column], errors='coerce')
        table2[column] = pd.to_numeric(table2[column], errors='coerce')
        stats1 = get_stats(table1[column])
        stats2 = get_stats(table2[column])
        counter_stats_table1 = dict(zip(['Average', 'Median', '95th percentile'], stats1))
        counter_stats_table2 = dict(zip(['Average', 'Median', '95th percentile'], stats2))

        counter_single_table = pd.DataFrame([counter_stats_table1, counter_stats_table2], index=['Last', 'New'])
        temp_dir_path = f'Temp\dir_{idx}'
        os.makedirs(temp_dir_path, exist_ok=True)
        counter_single_table.to_html(os.path.join(temp_dir_path, 'details.html'))


        values = (round((x - y) / x, 2) if abs(x - y) != 0 else 0 for x, y in zip(stats1, stats2))
        stats[idx] = (column, *values)
    data_table = pd.DataFrame.from_dict(stats, orient='index',
                                        columns=['Counter', 'Average', 'Median', '95th percentile'])
    style = data_table.style\
        .format(format_percents, subset=data_table.columns[1:])\
        .hide_index()\
        .set_properties(**{'text-align': 'right'}, subset=data_table.columns[1:])
        #.applymap(color_red, subset=data_table.columns[1:])

    with open('output.html', 'w') as fd:
        fd.write(style.render(table_title="Extending Example"))
    #data_table.to_html('output.html')
    #webbrowser.open_new('output.html')

    MyStyler = Styler.from_custom_template("", "html.tpl")

    with open('new.html', 'w') as fd:
        fd.write(MyStyler(data_table).render(table_title="Extending Example"))
    webbrowser.open_new('new.html')


if __name__ == '__main__':
    f1 = 'Counters_12100533.csv'
    f2 = 'Counters_12100649.csv'
    run(f1, f2)
