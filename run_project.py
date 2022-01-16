import os
from backend.app import db, add_admin
import subprocess
from multiprocessing import Process, Pool


# This block of code enables us to call the script from command line.
def execute(process):
    os.system(f'python {process}')


def run_backend():
    os.system('python backend/app.py')


def run_telegram_bot():
    os.system('python backend/telegram_bot.py')


def run_npm():
    subprocess.check_call('npm start --scripts-prepend-node-path=auto')

if __name__ == '__main__':
    # create all tables
    db.create_all()

    # create initial admin
    add_admin(username="admin", password="236369")

    # Creating the tuple of all the processes
    all_processes = ('backend/app.py', 'backend/telegram_bot.py')

    process_pool = Pool(processes=2)
    process_pool.map(execute, all_processes)

    '''p1 = Process(target=run_backend(), args=())
    p2 = Process(target=run_telegram_bot(), args=())
    p3 = Process(target=run_npm(), args=())
    
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()'''

