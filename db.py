#!/usr/bin/python

import sqlite3
from time import time
from datetime import datetime

db_name = "test.db"

def create_db():
    assert __name__=="__main__"
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        c.execute('''DROP TABLE 'plays';''');
        c.execute('''CREATE TABLE 'plays' (Id INTEGER PRIMARY KEY AUTOINCREMENT, DJ TEXT, Song TEXT, Date INTEGER );''');
        conn.commit();

def get_rows(print_=False):
    a = -1;
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        c.execute('''SELECT Count(*) as 'num' FROM plays;''');
        a = c.fetchone()[0]
        if print_:
            print("W bazie danych znajdują się %d rekordów" % a)
    return a

def get_day(timestamp = int(time()) ):
    timestamp_low = timestamp - (timestamp % 86400) # 86400 is number of seconds a day
    timestamp_high = timestamp_low + 86400
    print("data pobrana z bazy danych to %s." % datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d'))
    res = []
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        db = c.execute('''SELECT Id, DJ, Song, Date  FROM 'plays' WHERE date BETWEEN ? AND ?;''', (timestamp_low, timestamp_high))
        for data in db:
            p = Play();
            p.id = data[0]
            p.DJ = data[1]
            p.song = data[2]
            p.date = data[3]
            res.append(p)
    return res

    
class Play:
    id = None
    DJ = ""
    song = ""
    date = 0
    
    def __init__(self, DJ = None, song = None, date=int(time())):
        self.DJ = DJ
        self.song = song
        self.date = date 
            
    def save(self):
        with sqlite3.connect(db_name) as conn:
            c = conn.cursor()
            if self.id is None:
                c.execute('''INSERT INTO 'plays' (DJ, Song , Date ) VALUES (?,?,?);''', (self.DJ, self.song, self.date));
                self.id = c.lastrowid
                print("saved with id=%s" % str(self.id))
            else:
                c.execute('''UPDATE plays SET DJ = ?, Song=?, Date=? WHERE Id=?;''', (self.DJ, self.song, self.date, self.id));
            conn.commit();
            
    #check the status of Play class
    # 0 -> Object is saved, all is ok
    # 1 -> Object is not updated, call save function
    # 2 -> Object is not saved, call save function
    def check(self):
        if self.id is None:
            return 2
        with sqlite3.connect(db_name) as conn:
            c = conn.cursor()
            res = c.execute('''SELECT Count(*) as 'num' FROM 'plays' WHERE Id=? AND DJ=? AND Song=? AND Date=? ;''', (self.id, self.DJ, self.song, self.date)).fetchone()[0]
            if res == 0:
                return 1;
        return 0;
        
    def delete(self):
        if self.id is None:
            return 1
        with sqlite3.connect(db_name) as conn:
            c = conn.cursor()
            c.execute('''DELETE FROM 'plays' WHERE Id=?;''', (self.id,));
            conn.commit();
        self.id = None
        return 0
    

if __name__ == "__main__":
    
                                      #    tests   #
    
    a = get_rows()
    b = Play(DJ = "DJ", song = "test", date = 0);
    b.save();
    if not a+1 == get_rows():
        print("failed test 1");
    else:
        print("passed test 1");
        
        
    b.save()
    if a+2 == get_rows():
        print("failed test 2");
    else:
        print("passed test 2");
        
        
    d = Play(DJ="DeeJay", song="joke",date=0)
    if(d.check()==2):
        print("passed test 3");
    else:
        print("failed test 3");
        
        
    d.save();
    if(d.check()==0):
        print("passed test 4");
    else:
        print("failed test 4");
        
        
    d.date = 1
    if(d.check()==1):
        print("passed test 5");
    else:
        print("failed test 5");
        
        
    d.save();
    if(d.check()==0):
        print("passed test 6");
    else:
        print("failed test 6");
        
    b.delete();
    if(b.check()==2):
        print("passed test 7");
    else:
        print("failed test 7");        
