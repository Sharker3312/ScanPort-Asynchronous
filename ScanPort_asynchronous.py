#!/usr/bin/python3

import socket, os, time, pyfiglet,sys,urllib,asyncio,re,subprocess
from os import system
from datetime import datetime
from os import name, truncate





####HELP_Panel

if len(sys.argv) !=2:
    print("\n[i] Uso: python3 " + "sys.argv[0]"+ " < ip_adress>\n" )
    sys.exit(1)
###################################

ip_adress=sys.argv[1]
port_list=[]
open_ports=[]

##Saber sistema operativo
def get_ttl(ip):
     
    
    proc= subprocess.Popen(["/usr/bin/ping -c 1 %s" %ip_adress , "" ], stdout=subprocess.PIPE, shell=True)
    (out,err)=proc.communicate() 
    
    out=out.split()

    out=out[12].decode('utf-8')
     
    ttl_value = re.findall(r"\d{1,3}", out)[0]
    
    return ttl_value

def get_OS(ttl):
    
    ttl=int(ttl)
    if ttl >=0 and ttl <= 64:
        return "LINUX"
    elif ttl >= 65 and ttl <=128:
        return "WINDOWS"
    else:
        return "Not Found"
    
def what_OS():
    #ip_adress=sys.argv[1] 
    ttl=get_ttl(ip_adress)  
    os_name=get_OS(ttl)
    print("O.S -> |",os_name,"|")
###########################################################################################

for port in range(0,10000):
    port_list.append(port)
    

def banner():
    ascii_banner= pyfiglet.figlet_format("ScanPort")
    print(ascii_banner)
    print("    made by Sharker3312")
    print("-" *50)
    print("Scanning Target: " + ip_adress )
    print("Scanning Target at: "+str(datetime.now()))
    print("-"*50)
    
    
def clear():
    if os.name =="nt":
        os.system("cls")
    else:
        os.system("clear")  


async def check_port(ip, port, loop):
    
    conn = asyncio.open_connection(ip_adress, port, loop=loop)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=3)
        open_ports.append(port)
    except:
        print("",end="\r")
    finally:
        if 'writer' in locals():
            writer.close()
            
async def check_port_sem(sem, ip, port, loop):
    async with sem:
        return await check_port(ip, port, loop)
    
async def run(dests, ports, loop):
    
    sem = asyncio.Semaphore(1000)     #Change this value for concurrency limitation 
    tasks = [asyncio.ensure_future(check_port_sem(sem, d, p, loop)) for d in dests for p in ports]
    #for i in range(0,10000):
       # porc=float(i/10000)*100
       # porc=round(porc, 1)
        #print(porc,"%",end="\r")
        #time.sleep(0.005)
    
    responses = await asyncio.gather(*tasks)
    return responses

def menu():
    clear()
    banner()
    dests = [ip_adress] #destinations 
    ports = port_list #ports 
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(dests, ports, loop))
    loop.run_until_complete(future)
    print(open_ports,"-> OPEN")
    what_OS()
    print('-'*50)

    

if __name__=='__main__':
    
    menu()
    