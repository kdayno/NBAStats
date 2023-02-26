import pandas as pd


def generate_create_table_sql_script(dataframe, table_name: str, connection):
    """
    Generates Create Table SQL script in given SQL-flavour
    """

    ddl = pd.io.sql.get_schema(dataframe, table_name, con=connection)

    with open(f'{table_name}.sql', 'w') as f:
        f.write(ddl)


def move_col(df, cols_to_move=[], ref_col='', place='After'):
    """
    Rearranges dataframe columns to specified order
    """

    cols = df.columns.tolist()
    if place == 'After':
        seg1 = cols[:list(cols).index(ref_col) + 1]
        seg2 = cols_to_move
    if place == 'Before':
        seg1 = cols[:list(cols).index(ref_col)]
        seg2 = cols_to_move + [ref_col]

    seg1 = [i for i in seg1 if i not in seg2]
    seg3 = [i for i in cols if i not in seg1 + seg2]

    return(df[seg1 + seg2 + seg3])
