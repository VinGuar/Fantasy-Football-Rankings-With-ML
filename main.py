import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import time
from unidecode import unidecode
import numpy as np

df = pd.read_csv('161718Grades.csv')


print(df.to_string()) 




