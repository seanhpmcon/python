import pyodbc
import requests

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
        print(row[0])

    conn.commit()
    local_conn.commit()
    cursor.close()
    local_cursor.close()
    
def string_to_list(input_string):
    badges = input_string.split(',')

    cleaned_badges = [badge.strip() for badge in badges]

    return cleaned_badges