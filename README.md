# gbc-paste

## Setup
* Install Python 3.7.0
* `pip install Pillow`

## Usage
1. Paste name
```
python paste.py [ex. 林子雋] [output.png] --student
```
2. Send mail: note that the program will ask you if the greeting card is correct and appears as you expect.
```
python sendmail.py --check_greeting_card --student name_list.csv ./gathering1.png 2019.10-12.png output.png
```

## Demo
* `python paste.py 林子雋 output.png --student`:
    * Before: ![base.png](base.png)
    * After: ![output.png](output.png)
* `python sendmail.py --check_greeting_card --student name_list.csv ./gathering1.png 2020.07-09.png output.png`
    * ![email0](./demo/email-demo-0.png)
    * ![email1](./demo/email-demo-1.png)
