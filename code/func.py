import sqlite3


def f_addPersontodb(name, surname, age, year, info, path_photo):
    con = sqlite3.connect('../person_db.sqlite')
    cur = con.cursor()
    cur.execute(f"""INSERT INTO person(name, surname, age, year, information, photo)
    VALUES('{name}', '{surname}', {age}, DATE('{year}'), '{info}', '{path_photo}')""")
    con.commit()
    con.close()


def f_addVideotodb(datetime, peoples, not_known, video_path):
    date = datetime.toString('yyyy-MM-dd')
    time = datetime.toString('hh:mm:ss')

    a = list(peoples)
    if not not_known:
        a.append(f'неизвестные: {not_known}')
    people = ', '.join(a)

    con = sqlite3.connect('../person_db.sqlite')
    cur = con.cursor()
    cur.execute(f"""INSERT INTO videos(data, time, people, video)
        VALUES(DATE('{date}'), TIME('{time}'), '{people}', '{video_path}')""")
    con.commit()

    res = cur.execute("""SELECT * FROM videos""").fetchall()
    print(res)
    con.close()

