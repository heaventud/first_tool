import itertools
import pandas as pd
import sys
from configparser import ConfigParser


def get_stats(array):
    return array.mean(), array.median(), array.quantile(.95)


def write_to_html_file(df, title='', filename='output.html'):
    result = """
<html>
<head>
<style>

    h2 {
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
    }
    table { 
        margin-left: auto;
        margin-right: auto;
    }
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
    th, td {
        padding: 5px;
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
        font-size: 90%;
    }
    table tbody tr:hover {
        background-color: #dddddd;
    }
    .wide {
        width: 90%; 
    }

</style>
</head>
<body>
    """
    result += '<h2> %s </h2>\n' % title
    if type(df) == pd.io.formats.style.Styler:
        result += df.render()
    else:
        result += df.to_html(classes='wide', escape=False)
    result += """
</body>
</html>
"""
    with open(filename, 'w') as f:
        f.write(result)


def run(filename1, filename2):
    """
    """
    table1 = pd.read_csv(filename1)
    table2 = pd.read_csv(filename2)
    table1.columns = table1.columns.str.replace("\\", "_").str.replace("^__", "", regex=True)
    table2.columns = table2.columns.str.replace("\\", "_").str.replace("^__", "", regex=True)
    print("\n\t".join([f'{k} * {v}' for k, v in list(zip(itertools.count(1), table1.columns))]))
    num = int(input("pick number of counter: "))
    counter_name = table1.columns[num]
    header = '{:15} | {:^12} | {:^12} | {:^12}'.format(counter_name, 'Average', 'Median', '95th percentile')
    print('_' * len(header), end='')
    print(header, end='')
    print('_' * len(header))
    arr1 = pd.to_numeric(table1[counter_name], errors='coerce')
    arr2 = pd.to_numeric(table2[counter_name], errors='coerce')
    stats1 = (filename1, *get_stats(arr1))
    stats2 = (filename2, *get_stats(arr2))
    fmt = '{:%s} | {:12.2f} | {:12.2f} | {:12.2f}' % str(len(counter_name))
    print(fmt.format(*stats1))
    print(fmt.format(*stats2))


if __name__ == '__main__':
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    run(f1, f2)
