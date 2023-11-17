import pyodbc
from typing import List

def auth_user(user):
    conn_str = ("Driver={ODBC Driver 17 for SQL Server};Server=TTBRCDB001;Database=ZKCVBS_PRD;UID=zkcvbs_rpt_svc;PWD=mdmAMg3K$j#D^c~EXUYoJo%9V2zq$F;")

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    res = cursor.execute("""select au.username, ar.code
                            from [dbo].[auth_user] au
                            left join [dbo].[auth_user_role] aur on au.id = aur.auth_user_id
                            left join [dbo].[auth_role] ar on aur.auth_role_id = ar.id
                            where ar.code in ('administrator') or au.is_superuser = 1""")

    users: List[int] = []

    for row in res.fetchall():
        users.append(row[0])

    conn.commit()
    cursor.close()

    if user in users:
        return True
    else:
        return False