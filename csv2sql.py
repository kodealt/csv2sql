import csv
import sqlite3
import tkinter as tk
from tkinter import filedialog
import requests
import time
import os

csvFile = None
location =  os.path.abspath(__file__)
folderDirSave = os.path.dirname(location)
print(folderDirSave)
# with open(csvFile) as readTScsv:
#     reader = csv.DictReader(readTScsv)
#     for row in reader:
#         csvData.append(row)

def convert(csvFile = None):

    global csvData
    csvData = []
    errors = []

    startTime = time.time()

    sequel = sqlite3.connect(os.path.join(folderDirSave, "anime.db"))
    cursor = sequel.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS anime (
                   name TEXT NOT NULL PRIMARY KEY,
                   indexing INTEGER,
                   watched INTEGER,
                   tags TEXT,
                   rating REAL,
                   airing TEXT,
                   status TEXT,
                   days TEXT,
                   time TEXT,
                   startDate TEXT,
                   endDate TEXT,
                   priority INTEGER,
                   episodes INTEGER,
                   duration TEXT,
                   titleEn TEXT,
                   titleJp TEXT
                   )
""")

    with open(csvFile) as dictFile:
        reader = csv.DictReader(dictFile)

        for row in reader:
            csvData.append(row)

    theLength = len(csvData)
    previewInfo.config(text=f"please wait... \nindexing through list to add \nadditional information...\n will take roughly {round((theLength) * 1.1, 1)} seconds...\n do NOT close, or progress will be lost", font=("Arial", 10))

    for j, i in enumerate(csvData, start=1):
        try:
            response = requests.get(f"https://api.jikan.moe/v4/anime?q={i['NAME'].strip()}&limit=1", timeout=60)
            response.raise_for_status()
            results = response.json().get('data',[])
            if not results:
                raise ValueError(f"{i['NAME']} not found")

            anime = results[0]

            try:
                rating = float(i.get('RATING', 0.0))
            except ValueError:
                rating = 0.0

            airing = anime['airing']
            status = anime['status']
            days = anime['broadcast']['day']
            times = f"{anime['broadcast']['time']} (JST)"
            startDate = anime['aired']['from']
            endDate = anime['aired']['to']
            priority = 0
            episodes = anime.get('episodes', 0)
            duration = anime.get('duration', 'Unknown')
            titleEn = anime.get("title_english", "N/A")
            titleJp = anime.get("title_japanese", "N/A")

            cursor.execute(f"INSERT OR REPLACE INTO anime (name, indexing, watched, tags, rating, airing, status, days, time, startDate, endDate, priority, episodes, duration, titleEn, titleJp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (i['NAME'], i['INDEX'], i.get('VALUE', 0), i.get('TAGS', ''), rating, airing, status, days, times, startDate, endDate, priority, episodes, duration, titleEn, titleJp))
        
            print(f'{i["NAME"]} done. ~{round((theLength - j) * 1.1, 1)} seconds remaining ({j}/{theLength})')
            previewInfo.config(text=f'{i["NAME"]} done. ~{round((theLength - j) * 1.1, 1)} seconds remaining ({j}/{theLength})')

            time.sleep(1.1)

        except Exception as e:
            print(f"error at processing {i['NAME']} : {e}")
            previewInfo.config(text=f"error at processing {i['NAME']} : {e}")
            errors.append(f"error at processing {i['NAME']} : {e}")

    sequel.commit()
    sequel.close()

    endTime = time.time()
    elapsedTime = endTime - startTime
    
    print("\n\nerrors:")
    print("\n".join(e for e in errors))

    previewInfo.config(text=f"completed in {elapsedTime:.2f} seconds", font=('Arial', 15))
    print(f"completed in {elapsedTime:.2f} seconds")


def selectFile(askTitle = None, texLabel = None, fileType = None):
    global pathTS
    global folderDirSave
    if fileType == "folders":
        folderDirSave = filedialog.askdirectory(title= askTitle)
        saveTo.config(text=f"save DB to {folderDirSave}")
        return
    pathTS = filedialog.askopenfilename(
        title = askTitle,
        filetypes=[("Comma Seperated Values", "*.csv"), ("All Files", "*.*")]
    )

    if pathTS:
        texLabel.config(text = f"{pathTS}")

        tsDataIcl = []

        with open(pathTS) as dictFile:
            reader = csv.DictReader(dictFile)
            header = next(reader)
            for row in reader:
                tsDataIcl.append(row)
        
        preview(tsDataIcl)
    
    else:
        texLabel.config(text = "none selected")

def preview(file = None):
    if type(file) is list:
        previewInfo.config(text="\n".join(str(f) for f in file), font=("Arial", 5))

root = tk.Tk()
root.title("Csv To SQL")
root.geometry("350x450")
root.configure(bg = "#1C1C1C")

csvLabel = tk.Label(root, text="csv: none selected", fg = "white", bg="#1C1C1C"); csvLabel.pack(padx = 0, pady=10)
csvButton = tk.Button(root, text="select a csv file", fg = "white", bg="#1C1C1C", command = lambda: selectFile(askTitle="Select a csv file", texLabel=csvLabel, fileType = "csv")); csvButton.pack(padx=0, pady=10)

saveTo = tk.Label(root, text=f"save DB to {folderDirSave}", fg="white", bg="#1C1C1C"); saveTo.pack(padx=10, pady=10)
saveButton = tk.Button(root, text="choose a save path", fg = "white", bg="#1C1C1C", command = lambda: selectFile(askTitle="Select a csv file", texLabel=csvLabel, fileType = "folders")); saveButton.pack(padx=10, pady=10)

convertTs = tk.Button(root, text="convert to a Database", fg="white", bg="#1C1C1C", command=lambda:convert(csvFile = pathTS))
convertTs.pack(padx=10, pady=10)

previewInfo = tk.Label(root, text="", fg="white", bg="#1C1C1C"); previewInfo.pack(padx=10, pady=10)

root.mainloop()