from dataFetch import UbuntuCPUData, UbuntuMemData
import time, sqlite3, os

dataDuration, plotPoints, plotDivisor = 5, 60, 5 #default is 5, 60, 5 which translates to 60 points of data every 5 seconds and the subsequent chart will be divided by 5.
#hardcoding the points, divisor and duration isn't ideal, but it at least allows multiples of itself. might update this in future

def dbUpdate():
    if not os.path.exists("Database.db"): #first time setup catch
        conn = sqlite3.connect("Database.db") #connects to db, creates db if doesn't exist in current working directory
        cur = conn.cursor() #initialises a cursor for interacting with SQLite db
        cur.execute("CREATE TABLE DBCPUData(id integer primary key, cpu REAL, time TEXT)") 
        cur.execute("CREATE TABLE DBMemData(id integer primary key, mem REAL, time TEXT)")
        #create tables, id is unique & primary key, date is currently just a string (but is spat out of dataFetch in a useable format)
        
    conn = sqlite3.connect("Database.db") #connects to db, creates db if it doesn't exist in current working directory
    cur = conn.cursor() #initialises a cursor for interacting with SQLite db
    
    while True:
        try:
            currentCPU = UbuntuCPUData()
            currentMem = UbuntuMemData() #initialise objects from dataFetch.py
            cur.execute("INSERT INTO DBCPUData(cpu, time) VALUES (?, ?)", (currentCPU.processData()[0], currentCPU.processData()[1]))
            conn.commit()
            cur.execute("INSERT INTO DBMemData(mem, time) VALUES (?, ?)", (currentMem.processData()[0], currentCPU.processData()[1])) 
            #where currentMem.processData[0] = int.int, currentCPU.processData[0] = string (PURPOSELY USING CPU TIMESTAMP FOR BOTH FOR UNIFORMITY)
            conn.commit()

        except Exception as e:
            print(f"Error updating database: {e}")

        time.sleep(dataDuration)

if __name__ == '__main__':
    print("dbExec is running.")
    dbUpdate()
