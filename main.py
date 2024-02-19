from flask import Flask, render_template
from dataFetch import UbuntuCPUData, UbuntuMemData
from dbExec import dataDuration, plotPoints, plotDivisor
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time, sqlite3, subprocess, os

app = Flask(__name__) #initialise Flask app object
app.config["SECRET_KEY"] = "my secret"

@app.route('/home')
def home():
    conn = sqlite3.connect("file:Database.db?mode=ro", uri=True) #connects to db (read only mode)
    cur = conn.cursor() #initialises a cursor object for interacting with SQLite db
    
    fetchCPU = cur.execute(f"SELECT cpu FROM DBCPUData ORDER BY id DESC LIMIT {plotPoints};").fetchall()
    fetchMem = cur.execute(f"SELECT mem FROM DBMemData ORDER BY id DESC LIMIT {plotPoints};").fetchall()
    fetchCPUTime = cur.execute(f"SELECT time FROM DBCPUData ORDER BY id DESC LIMIT {plotPoints};").fetchall()
    fetchMemTime = cur.execute(f"SELECT time FROM DBMemData ORDER BY id DESC LIMIT {plotPoints};").fetchall() #there is likely a better way of doing this, as the queries return [(data,), (data,), (data,) ... ] which is painful to unpack
    plot(fetchCPU, fetchMem, fetchCPUTime, fetchMemTime) #plots the data

    return render_template('Home.html', 
                           fiveMinCPU=fetchCPU[0][0], 
                           fiveMinMem=fetchMem[0][0], 
                           fiveMinCPUTime=fetchCPUTime[0][0].split('.')[0],
                           fiveMinMemTime=fetchMemTime[0][0].split('.')[0]) #renders the Home.html template with the respective data [(data,), (data,), (data,) ... ] 

def plot(cpu, mem, cpuTime, memTime):
    fiveMinCPU = []
    for i in range(0, plotPoints, 1):
        try: fiveMinCPU.append(cpu[i][0])
        except IndexError: continue
    fiveMinMem = []
    for i in range(0, plotPoints, 1):
        try: fiveMinMem.append(mem[i][0])
        except IndexError: continue
    fiveMinCPUTime = []
    for i in range(0, plotPoints, 1):
        try: fiveMinCPUTime.append(memTime[i][0])
        except IndexError: continue
    fiveMinMemTime = []
    for i in range(0, plotPoints, 1):
        try: fiveMinMemTime.append(memTime[i][0]) #
        except IndexError: continue
    #the SQLite database queries from thefetchCPU, fetchCPUTime, fetchMem and fetchMemTime 
    #all return [(data,)] unfortunately

    plt.clf() #clears the last plot drawn (if there is one)
    fig, ax = plt.subplots()  # Create a figure and an axes object
    ax.plot(fiveMinCPUTime, fiveMinCPU[::-1], color = "blue") 
    ax.plot(fiveMinMemTime, fiveMinMem[::-1], color = "green") #[::-1] is a slicing practice to invert the list, otherwise it plots in the wrong direction
    ax.fill_between(fiveMinCPUTime, fiveMinCPU[::-1], color="blue", alpha=0.3)
    ax.set_xlabel("Time (Seconds)")
    ax.set_ylabel("CPU + Mem Utilisation (%)")
    ax.set_xticks([i for i in range(0, plotPoints+(int(plotPoints/plotDivisor)), int(plotPoints/plotDivisor))])
    ax.set_xticklabels([i for i in range(int(plotPoints*dataDuration), 0-(int(plotPoints/plotDivisor)), -(plotPoints))])
    ax.set_xlim(0, plotPoints)
    ax.set_ylim(0, 100)
    ax.margins(0, 0)
    plt.savefig(os.path.join("static", "images", "plot.svg"), bbox_inches="tight") #bbox arg is for removing white space around the plot

if __name__ == '__main__':
    print("UbuntuDash is running.\nPUSH CTRL + C TO END\nPUSH CTRL + C TO END\nPUSH CTRL + C TO END\n")
    process = None
    try:
        process = subprocess.Popen(("python3", "dbExec.py"), shell=False)
        time.sleep(3) #small delay while dbExec creates directories and initialises etc.
        app.run(host='127.0.0.1', port=8000, debug=False)
    except KeyboardInterrupt: #dbExec will end at the same time as main.py
        if process is not None:
            process.terminate()
            print("UbuntuDash is stopped.")
            process.wait() # Ensure the process is fully terminated before exiting
    print("UbuntuDash is stopped.")
