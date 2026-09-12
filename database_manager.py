import time
import _thread
import pickle
import random


def print_status(db_manager):
    while(True):
        print("\nCurrently there are %d reading processes..."%db_manager.read_access_counter)
        time.sleep(3)

def simulate_process_reading_from_DB(db_content):
    time.sleep(random.randint(10,20))
    return

'''
This class is responsible for accessing the database (for read/write operations)
'''
class DB_IO (object):
    def __init__(self, _filename):
        self.filename = _filename

    def write_to_DB(self, dict_updates):
        with open(self.filename, 'rb') as fn:
            grds_dict = pickle.load(fn)

        for k,v in dict_updates.items():
            grds_dict[k] = v

        with open(self.filename, "wb") as fn:
            pickle.dump(grds_dict, fn)

    def read_from_DB(self, _DB_Manager):
        with open(self.filename, 'rb') as fn:
            grds_dict = pickle.load(fn)
            simulate_process_reading_from_DB(grds_dict)
            _DB_Manager.read_access_counter -= 1


'''
This class is managing the access permission to the database 
(according to the number of clients that are currently reading from/writing to database)
'''
class DB_Manager (object):
    def __init__(self, _filename):
        self.read_access_counter = 0
        self.write_access = False
        self.db_io = DB_IO(_filename)

    def request_read(self):
        if self.read_access_counter >= 10:
            print ("\naccess denied, 10 clients currently have reading access, please try again later...")
            return
        elif self.write_access == True:
            print("\naccess denied, there is already a client with write access, please try again later...")
            return
        else:
            print("\nread permission is granted")
            self.read_access_counter += 1
            _thread.start_new_thread(self.read_thread, ())

    def request_write(self, dict_to_update):
        if self.read_access_counter > 0:
            print("\nCan't grant writing access, there are %d processes reading, "
                  "waiting for them to terminate..."%self.read_access_counter)
        elif self.write_access == True:
            print("\naccess denied, there is a client that currently has a reading access, please try again later...")
        else:
            print("\nwrite permission is granted")
            self.write_access = True
            self.db_io.write_to_DB(dict_to_update)
            self.write_access = False

    def request3(self):
        if self.read_access_counter > 0:
            print ("\ncan't grant a read permission, a client currently have a reading access")
        return

    def request4(self, dict_to_update):
        if self.write_access == True:
            print("\naccess denied, there is a client that currently has a reading access, please try again later...")
        return

    def request5(self):
        if self.read_access_counter >= 9:
            print ("\naccess denied, 10 clients currently have reading access, please try again later...")
            return
        elif self.write_access == True:
            print("\naccess denied, there is already a client with write access, please try again later...")
            return
        else:
            self.read_access_counter += 2
            _thread.start_new_thread(self.read_thread, ())
            _thread.start_new_thread(self.read_thread, ())
        return

    def request6(self,dict_to_update):
        if self.write_access == True:
            print("\naccess denied, there is already a client with write access, please try again later...")
        elif self.read_access_counter <= 10:
            num = 10-self.read_access_counter
            while(num>0):
                self.read_access_counter += 1
                print("\nread permission is granted")
                _thread.start_new_thread(self.read_thread, ())
                num=num-1
        while(self.read_access_counter>0):
            print("\nCan't grant writing access, there are %d processes reading, "
                  "waiting for them to terminate..."%self.read_access_counter)

        print("\nwrite permission is granted")
        self.write_access = True
        self.db_io.write_to_DB(dict_to_update)
        self.write_access = False

        while self.write_access == True:
            print("\naccess denied, there is already a client with write access, please try again later...")

        i=10
        while(i>0):
            self.read_access_counter += 1
            print("\nread permission is granted")
            _thread.start_new_thread(self.read_thread, ())
            i=i-1

        return


    def read_thread(self):
        self.db_io.read_from_DB(self)

    def choose(self):
        request = input('''choose one of these tests (write the number of your request):
                 1.get read permission
                 2.get write permission
                 3.can't get read permission
                 4.can't get write permission
                 5.get multiple read permissions
                 6.can't get write permission until every process gives up on its read permission
                 7.terminate''')
        return request


if __name__ == '__main__':
    grades_dict = {'user_1': 11, 'user_2': 22, 'user_3': 33, 'user_4': 44, 'user_5': 55, 'user_6': 66, 'user_7': 77, 'user_8': 88, 'user_9': 99}
    filename = 'grades'
    outfile = open(filename, 'wb')
    pickle.dump(grades_dict, outfile)
    outfile.close()

    infile = open(filename, 'rb')
    curr_dict = pickle.load(infile)
    print(curr_dict)

    new_grades_dict = {'user_1': 12, 'user_2': 23, 'user_3': 34, 'user_4': 45, 'user_10': 0}
    db_manager = DB_Manager('grades')
    _thread.start_new_thread(print_status, (db_manager,))
    x = True
    while(x):
        request_number=db_manager.choose()
        if(request_number=='1'):
            db_manager.request_read()
        if(request_number=='2'):
            db_manager.request_write(new_grades_dict)
        if(request_number=='3'):
            db_manager.request3()
        if(request_number=='4'):
            db_manager.request4(new_grades_dict)
        if(request_number=='5'):
            db_manager.request5()
        if(request_number=='6'):
            db_manager.request6(new_grades_dict)
        if(request_number=='7'):
            print("bye")
            x=False

    '''
    infile = open(filename, 'rb')
    new_dict = pickle.load(infile)
    print(new_dict)
    infile.close()
    '''
