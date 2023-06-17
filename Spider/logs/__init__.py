import os
from datetime import date
import logging

current_path=os.path.dirname(__file__)
today=date.today()
file_name=os.path.join(current_path,f'WebSearch_{today}.log')
print(file_name)
logging.basicConfig(filename=file_name, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')