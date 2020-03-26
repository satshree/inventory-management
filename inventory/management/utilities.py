from django.conf import settings
from datetime import datetime
import os 

def log(*args):
    """ Log Error. """

    file_path = os.path.join(settings.BASE_DIR, 'exception_log')
    file_name = os.path.join(file_path, "Exception {}.txt".format(datetime.now().strftime("%Y %b. %d")))

    with open(file_name, "a") as file:
        file.write("")
        file.write("-" * 100)
        file.write("")
        file.write(datetime.now().strftime("%I:%H:%S %p"))
        file.write("")
        for log in args:
            line = log + " \n"
            file.write(line)
        
        file.write("-" * 100)
