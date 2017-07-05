import sqlite3 , datetime, time
from PIL import Image
conn = sqlite3.connect("instadb.db")
c = conn.cursor()
tableName='photodb'
def createTable():
    c.execute('CREATE TABLE IF NOT EXISTS ' + tableName + '(id INTEGER PRIMARY KEY, userid INTEGER, datestamp TEXT, photourl TEXT, tags TEXT)')

def putnewData(userid,date,url,tags):
    c.execute("INSERT INTO {} (userid, datestamp, photourl, tags) VALUES(?,?,?,?)".format(tableName), (userid, date, url, tags))
    print("DONE...")
    conn.commit()

def readData(userid):

    c.execute("SELECT * FROM {} WHERE userid = ?".format(tableName),(userid,))
    res=c.fetchall()
    if len(res) == 0:
        print('No records found')
        return

    for row in res:
        img = Image.open(row[3])
        img.show()
        #print(row[3])
        tags=row[4]
        print('Tags associated:',tags)


def updateData():
    id=input("Enter User Id:")
    c.execute("SELECT * FROM {} WHERE userid = ?".format(tableName),(id,))
    result=c.fetchall()
    if len(result) == 0:
        print('No Records Found...')
        return
    for row in result:
        print('Id:{} and Url:{}'.format(row[0],row[3]))
    id = int(input('Enter the id whose data is to be updates:'))
    c.execute("Update {} Set photourl = (?), tags = (?) where id = (?)".format(tableName),
              (input("Please input the correct path of the image:"),
               input("Please enter tags if any seperated by (,)...(Enter None) if none:") ,id,))
    conn.commit()
    print('DATA UPDATED...')

def deleteData():
    id = input("Enter User Id:")
    c.execute("SELECT * FROM {} WHERE userid = ?".format(tableName), (id,))
    result = c.fetchall()
    if len(result) == 0:
        print('No Records Found...')
        return
    for row in result:
        print('Id:{} and Url:{}'.format(row[0], row[3]))
    id = int(input('Enter the id whose data is to be updates:'))
    c.execute("DELETE FROM {} WHERE id = (?)".format(tableName), (id,))
    conn.commit()

def DeleteAll():
    c.execute("DELETE FROM {}".format(tableName))
    print('Item Deleted Successfully')
    conn.commit()
if __name__ == "__main__":

    createTable()
    while True:
        option = int(input(
            '1. Insert data to InstaDb\n2.Update Data in instaDb\n3.Search photo through tags or userId\n4.Delete data from instaDB\n5.Exit '))
        if option is 5:
            break

        if option is 1:
            userid=input("userID:")
            date = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
            photourl = input("Please input the correct path of the image:")
            tags= input("Please enter tags if any seperated by (,)...(Press None) if None:")
            putnewData(userid,date,photourl,tags)
        elif option is 3:
            id = input("Enter the user id to view photos")
            readData(id)
        elif option is 2:
            updateData()
        elif option is 4:
            deleteData()
        else:
            print('Invalid input.. TryAgain')
    c.close()
    conn.close()