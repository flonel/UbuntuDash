<div align="center">
	<h3>UbuntuDash is a lightweight, synchronous Flask dashboard for Linux utilising an SQLite database.</h3>
</div>

## About
- This is my first ever Python project published to GitHub. It's mainly a proof of concept having learnt lots of different skills.

- UbuntuDash has an (albeit basic) custom module for fetching CPU% and Mem% data via Bash commands.

- The chart logs every 5 seconds for a total of 5 minutes of history (similar to Windows 10's task manager).


![Ver 1 0 0](https://github.com/flonel/UbuntuDash/assets/135614626/af7aeeeb-ea22-42a9-a45a-f36233c4469a)

## Dependencies:

- UbuntuDash was developed for Ubuntu Server 20.04 LTS (but hopefully will run on any Linux distro).

[**Flask:**](https://flask.palletsprojects.com/en/3.0.x/)

```
$ pip install Flask
```

[**Matplotlib:**](https://matplotlib.org/stable/index.html)

```
$ pip install matplotlib
```

[**SQLite3:**](https://docs.python.org/3/library/sqlite3.html)

```
$ sudo apt install sqlite3
```

## Running
Within your Python3 environment and with the dependencies installed, simply run _main.py_:

```
$ python3 main.py
```

Then, within a browser, head to: 

`127.0.0.1:8000/home`

_**Due to the synchronous nature of this app, use F5 or refresh to fetch the latest data / graph.**_


To kill the server, simply push: 

⠀>>> <kbd>Ctrl</kbd> + <kbd>C</kbd>

## Disclaimer
Please note that this project features no consideration for security. This app is provided as-is, without any warranty or guarantee of its performance or suitability for any specific purpose.
