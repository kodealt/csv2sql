# csv2sql
This is a simple gui for my project, anime. This translates the previous CSV based data storing system to a much more efficient SQLite based Database storage.

<strong> ONLY USE THIS IF YOU HAVE USED THE VERSION 1 OF ANIME.py</strong>

# how to use ( EXE )

to use this, you can either use the pre-compiled code in the release. 

To use this version, install from the releases tab. 

Run the csv2py.exe

you will be greeted by a terminal and a gui. 

By default, the database file will save on the same folder as the exe. 

if you want to change the save path, select "choose a save path" button. this will bring up a prompt to change folders (recommended to do so in the same folder as the anime.py or anime.exe)

select the old csv. The "select a csv file" will allow you to navigate to the csv file.

after setting the save path and the csv file, press "convert to a Database"

the gui will not respond while it is converting. This is a flaw that i intend to fix when i have figured out its root cause. the terminal will show the progress, so please dont close the GUI, as you will need to restart the process. 

this process will take a while, as all of the titles in your list will have to go through the jikan.moe api to gather more information. The longer the list, the longer the time. [O(n)] 

after the database has been compiled, you can quit the GUI.

And thats it! you have the database file. If you have any issues with the app, feel free to send me a dm on discord : @a_persan

# how to use ( py ) 

the process is the same as the exe version, except you need to install some dependencies. aka just requests.

you also need to use python version 3.12.5 idk what other versions work. later should be fine. probably.

`pip install requests`
