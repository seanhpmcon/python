from numpy import NaN
import pandas as pd
import pyodbc
import requests
import jellyfish
from typing import List, Dict

def remove_emp(emp_no, user):

    conn_str = ("Driver={ODBC Driver 17 for SQL Server};Server=TTBRCDB001;Database=ZKCVBS_PRD;UID=zkcvbs_rpt_svc;PWD=mdmAMg3K$j#D^c~EXUYoJo%9V2zq$F;")
    
    local_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=QPPSL-WS-13;DATABASE=zk_logs;Trusted_Connection=yes;')

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    local_cursor = local_conn.cursor()
    
    insert_query = "INSERT INTO empl_unenroll (pin, first_name, last_name, clock_number, created_by) VALUES (?, ?, ?, ?, ?)"

    res = cursor.execute("""select aa.code, pp.name, pp.last_name
    from [dbo].[auth_area] aa
    left join [dbo].[auth_area] aa1 on aa.parent_id = aa1.id
    join [dbo].[att_area_person] aap on aa.id = aap.auth_area_id
    join [dbo].[pers_person] pp on aap.pers_person_id =pp.id
    join [dbo].[auth_department] ad on pp.auth_dept_id = ad.id
    where pp.pin = '%s'""" % (emp_no))

    for row in res.fetchall():
        requests.post('https://security.pmcon.co.tt/api/attAreaPerson/delete?access_token=11A61DC602A18E97E1A52CD37099F7BFFFD2A1769F1B6CA1F5375159F42B2D5C', json={
            "code": str(row[0]),
            "pins": [int(emp_no)]
        }, verify=False)
        local_cursor.execute(insert_query, emp_no, row[1], row[2], row[0], f"zkuser - {user}")

    conn.commit()
    local_conn.commit()
    cursor.close()
    local_cursor.close()
    
def remove_excel_emp(emp_no, user):

    conn_str = ("Driver={ODBC Driver 17 for SQL Server};Server=TTBRCDB001;Database=ZKCVBS_PRD;UID=zkcvbs_rpt_svc;PWD=mdmAMg3K$j#D^c~EXUYoJo%9V2zq$F;")
    
    local_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=QPPSL-WS-13;DATABASE=zk_logs;Trusted_Connection=yes;')

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    local_cursor = local_conn.cursor()
    
    insert_query = "INSERT INTO empl_unenroll (pin, first_name, last_name, clock_number, created_by) VALUES (?, ?, ?, ?, ?)"

    res = cursor.execute("""select aa.code, pp.name, pp.last_name
    from [dbo].[auth_area] aa
    left join [dbo].[auth_area] aa1 on aa.parent_id = aa1.id
    join [dbo].[att_area_person] aap on aa.id = aap.auth_area_id
    join [dbo].[pers_person] pp on aap.pers_person_id =pp.id
    join [dbo].[auth_department] ad on pp.auth_dept_id = ad.id
    where pp.pin = '%s'""" % (emp_no.iloc[0]))

    for row in res.fetchall():
        if jellyfish.jaro_distance(emp_no.iloc[1].lower(),row[1].lower()) > 0.7 and jellyfish.jaro_distance(emp_no.iloc[2].lower(),row[2].lower()) > 0.7:
            requests.post('https://security.pmcon.co.tt/api/attAreaPerson/delete?access_token=11A61DC602A18E97E1A52CD37099F7BFFFD2A1769F1B6CA1F5375159F42B2D5C', json={
                "code": str(row[0]),
                "pins": [int(emp_no.iloc[0])]
            }, verify=False)
            local_cursor.execute(insert_query, emp_no.iloc[0], row[1], row[2], row[0], f"zkuser - {user}")

    conn.commit()
    local_conn.commit()
    cursor.close()
    local_cursor.close()

def remove_by_clock(clock_no):

    conn_str = ("Driver={ODBC Driver 17 for SQL Server};Server=TTBRCDB001;Database=ZKCVBS_PRD;UID=zkcvbs_rpt_svc;PWD=mdmAMg3K$j#D^c~EXUYoJo%9V2zq$F;")

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    res = cursor.execute("""select pp.pin, pp.name, pp.last_name
                            from [dbo].[att_area_person] aap
                            join [dbo].[pers_person] pp on aap.pers_person_id = pp.id
                            join [dbo].[auth_area] aa on aap.auth_area_id = aa.id
                            where aa.code = '%s'""" % (clock_no))

    emps: List[int] = []

    for row in res.fetchall():
        emps.append(row[0])

    requests.post('https://security.pmcon.co.tt/api/attAreaPerson/delete?access_token=11A61DC602A18E97E1A52CD37099F7BFFFD2A1769F1B6CA1F5375159F42B2D5C', json={
        "code": str(clock_no),
        "pins": emps
    }, verify=False)

    conn.commit()
    cursor.close()

def get_areas():

    conn_str = ("Driver={ODBC Driver 17 for SQL Server};Server=TTBRCDB001;Database=ZKCVBS_PRD;UID=zkcvbs_rpt_svc;PWD=mdmAMg3K$j#D^c~EXUYoJo%9V2zq$F;")

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    res = cursor.execute("""select code, name
                            from [dbo].[auth_area]
                            """)

    clocks: Dict[int, str] = {}

    for row in res.fetchall():
        clocks[int(row[0])] = row[1]

    conn.commit()
    cursor.close()

    return clocks

def enroll_emp(badges):

    conn_str = ("Driver={ODBC Driver 17 for SQL Server};Server=TTBRCDB001;Database=ZKCVBS_PRD;UID=zkcvbs_rpt_svc;PWD=mdmAMg3K$j#D^c~EXUYoJo%9V2zq$F;")

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    res = cursor.execute("""select aa.code, pp.pin
                            from [pmcon].[dept_area_mapping] dam
                            join [dbo].[auth_area] aa on dam.auth_area_code = aa.code
                            join [dbo].[auth_department] ad on dam.auth_dept_code = ad.code
                            join [dbo].[pers_person] pp on ad.id = pp.auth_dept_id
                            where pp.pin in (%s)""" % (badges))

    clocks: Dict[int, List] = {}

    for row in res.fetchall():
        if int(row[0]) in clocks:
            clocks[int(row[0])].append(int(row[1]))
        else:
            clocks[int(row[0])] = []
            clocks[int(row[0])].append(int(row[1]))

    conn.commit()
    cursor.close()

    for k, v in clocks.items():
        requests.post('https://security.pmcon.co.tt/api/attAreaPerson/set?access_token=11A61DC602A18E97E1A52CD37099F7BFFFD2A1769F1B6CA1F5375159F42B2D5C', json={
        "code": str(k),
        "pins": v
        }, verify=False)

    return clocks

def upload_enrollf(df):
    emp_list = df[df.columns[0]].values.tolist()

    emp_string = ','.join([str(i) for i in emp_list])

    conn_str = ("Driver={ODBC Driver 17 for SQL Server};Server=TTBRCDB001;Database=ZKCVBS_PRD;UID=zkcvbs_rpt_svc;PWD=mdmAMg3K$j#D^c~EXUYoJo%9V2zq$F;")

    conn = pyodbc.connect(conn_str)

    sql = """select pp.pin, pp.name, pp.last_name, aa.code
    from [pmcon].[dept_area_mapping] dam
    join [dbo].[auth_area] aa on dam.auth_area_code = aa.code
    join [dbo].[auth_department] ad on dam.auth_dept_code = ad.code
    join [dbo].[pers_person] pp on ad.id = pp.auth_dept_id
    where pp.pin in (%s)""" % (emp_string)

    sql_df = pd.read_sql(sql, conn, dtype={'pin':int, 'name':str, 'last_name':str})

    # print(sql_df.info())
    merged_df = pd.merge(df, sql_df, left_on='employee_pin', right_on='pin', how='left').replace(NaN, '')

    def name_check(emp_no):
        if jellyfish.jaro_distance(emp_no.iloc[1].lower(),emp_no.iloc[4].lower()) > 0.7 and jellyfish.jaro_distance(emp_no.iloc[2].lower(),emp_no.iloc[5].lower()) > 0.7:
            return 1
        else:
            return 0
        
    merged_df['to_run'] = merged_df.apply(name_check, axis=1)

    merged_df = merged_df[merged_df['to_run'] == 1]

    grouped = merged_df.groupby("code")

    for area, group in grouped:
        if area != '':
            requests.post('https://security.pmcon.co.tt/api/attAreaPerson/set?access_token=11A61DC602A18E97E1A52CD37099F7BFFFD2A1769F1B6CA1F5375159F42B2D5C', json={
            "code": str(area),
            "pins": group['pin'].values.tolist()
            }, verify=False)

def clock_enrollf(clock, df):
    emp_list = df[df.columns[0]].values.tolist()

    emp_string = ','.join([str(i) for i in emp_list])

    conn_str = ("Driver={ODBC Driver 17 for SQL Server};Server=TTBRCDB001;Database=ZKCVBS_PRD;UID=zkcvbs_rpt_svc;PWD=mdmAMg3K$j#D^c~EXUYoJo%9V2zq$F;")

    conn = pyodbc.connect(conn_str)

    sql = """select pp.pin, pp.name, pp.last_name, aa.code
    from [pmcon].[dept_area_mapping] dam
    join [dbo].[auth_area] aa on dam.auth_area_code = aa.code
    join [dbo].[auth_department] ad on dam.auth_dept_code = ad.code
    join [dbo].[pers_person] pp on ad.id = pp.auth_dept_id
    where pp.pin in (%s)""" % (emp_string)

    sql_df = pd.read_sql(sql, conn, dtype={'pin':int, 'name':str, 'last_name':str})

    # print(sql_df.info())
    merged_df = pd.merge(df, sql_df, left_on='employee_pin', right_on='pin', how='left').replace(NaN, '')

    def name_check(emp_no):
        if jellyfish.jaro_distance(emp_no.iloc[1].lower(),emp_no.iloc[4].lower()) > 0.7 and jellyfish.jaro_distance(emp_no.iloc[2].lower(),emp_no.iloc[5].lower()) > 0.7:
            return 1
        else:
            return 0
        
    merged_df['to_run'] = merged_df.apply(name_check, axis=1)

    grouped = merged_df[merged_df['to_run'] == 1]

    requests.post('https://security.pmcon.co.tt/api/attAreaPerson/set?access_token=11A61DC602A18E97E1A52CD37099F7BFFFD2A1769F1B6CA1F5375159F42B2D5C', json={
    "code": str(clock),
    "pins": grouped['pin'].values.tolist()
    }, verify=False)
    
def string_to_list(input_string):
    badges = input_string.split(',')

    cleaned_badges = [badge.strip() for badge in badges]

    return cleaned_badges

def name_check(emp_no):
    if jellyfish.jaro_distance(emp_no.iloc[1].lower(),emp_no.iloc[4].lower()) > 0.7 and jellyfish.jaro_distance(emp_no.iloc[2].lower(),emp_no.iloc[5].lower()) > 0.7:
        return 1
    else:
        return 0