# Tool for visualising SLAM graph for mrob library

## How to run (Linux only now)

Install dependencies

```sudo apt install libcairo2-dev libgirepository1.0-dev libpython3-dev```

Create virtual env and install requirements

```
virtualenv -p python3 venv
source venv/bin/activate
pip install pip --upgrade
pip install -r requirements.txt
```

Now you can run the application

```commandline
python3 src/main.py
```

## Screenshot
![screenshot](https://github.com/alexandrsmirn/SLAM-visualization/blob/master/Screenshot.png)
