import pyodbc
import requests

def remove_emp(emp_no):

    conn_str = ("Driver={ODBC Driver 17 for SQL Server};Server=TTBRCDB001;Database=ZKCVBS_PRD;UID=zkcvbs_rpt_svc;PWD=mdmAMg3K$j#D^c~EXUYoJo%9V2zq$F;")

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    emp = emp_no

    res = cursor.execute("""select aa.code
    from [dbo].[auth_area] aa
    left join [dbo].[auth_area] aa1 on aa.parent_id = aa1.id
    join [dbo].[att_area_person] aap on aa.id = aap.auth_area_id
    join [dbo].[pers_person] pp on aap.pers_person_id =pp.id
    join [dbo].[auth_department] ad on pp.auth_dept_id = ad.id
    where pp.pin = '%s'""" % (emp))

    for row in res.fetchall():
        requests.post('https://security.pmcon.co.tt/api/attAreaPerson/delete?access_token=11A61DC602A18E97E1A52CD37099F7BFFFD2A1769F1B6CA1F5375159F42B2D5C', json={
            "code": str(row[0]),
            "pins": [int(emp)]
        }, verify=False)
        print(row[0])

    conn.commit()
    cursor.close()
    
def string_to_list(input_string):
    badges = input_string.split(',')

    cleaned_badges = [badge.strip() for badge in badges]

    return cleaned_badges