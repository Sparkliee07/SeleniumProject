import os
import paramiko
import logging
import time
import socket

# import module
from datetime import datetime


os.system("")  # enables ansi escape characters in terminal
mydict = {1:'6_pack_automation', 2:'10_pack_Manual'}

COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "YELLOW": "\033[93m",
    "LIGHTPURPLE" : "\033[94m",
    "PURPLE" : "\033[95m",
    "CYAN" : "\033[96m",
    "LIGHTGRAY" : "\033[97m",
    "BLACK" : "\033[98m",
    "WHITE": "\033[99m",
    "ENDC": "\033[0m",
}


# get current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
print("Current date & time : ", current_datetime)

# convert datetime obj to string
str_current_datetime = str(current_datetime)
# Append-adds at last
logFileName = 'GetSiteTemprature_' + str_current_datetime +'.csv'
file1 = open(logFileName, "w")  # append mode
Header = "Date and Time     , Site IP   , Diode1 , Diode2 , Diode3 , Diode4 , ColdPlate ThermalValue , ColdPlate ID , CoolentValve Value \n"  
#print(Header)
file1.write(Header)
file1.close()

        
def ssh_command(hostname, username, password, command):
    """Executes a command on a remote host via SSH."""

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        return output, error

    finally:
        client.close()
        
def log_to_file(message):
    """Logs a message to a file named 'ShhTest.log'."""
    file1 = open(logFileName, "a")  # append mode
    file1.write(message)
    file1.close()



def getSitetemprature(siteIp):
    #hostname = "192.168.1.1"
    hostname = siteIp
    username = "cpc"
    password = "Teradyne"
    # get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    # convert datetime obj to string
    str_current_datetime = str(current_datetime)
    #lamda to parse string
    split_string = lambda x, sep: x.split(sep)
    
    #write in to file    
    #result_Writeln = str_current_datetime + " :,    "+ str(siteIp) +",  " +str(DiodeTemp[0])+ ",    " + str(DiodeTemp[1])+ ",   " + str(DiodeTemp[2])+ ",   " + str(DiodeTemp[3])+ ",   " + str(CPThermalValue) + "\n"
    result_Writeln = str_current_datetime + ",    "+ str(siteIp) 
    
    #Display on Screen
    result_Println = str_current_datetime + " : " + COLOR["CYAN"]+ str(siteIp)+" : "+ COLOR["ENDC"]
    #print(result_Println)
    
    SiteStatus_res = ""
   
    try:
        command = "tsar GetSiteStatus"
        #output, error = ssh_command(hostname, username, password, command)
        output= "[NoFaults NoTesterFaults 3758096384 [[Fixed12V_2 0.014 0.17 NoPowerFaults] [Fixed12V_1 0.077 0.005 NoPowerFaults]] [12 [[SltbFan_1 3.236] [SltbFan_2 3.335] [SiteFan_1 5.128]] NaN 0 0 [22.234 67.354 71.555 59.363] NoThermalFaults] [TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success TER_Status_Success]]"
        error = None
        if error:
            print("Error:")
            print(error)
            result_Writeln += " , Error : " + error 
            log_to_file(result_Writeln)
    except:
        #print("An exception occurred")
        result_Writeln += " , Ssh Failure Site Fp may down" 
        log_to_file(result_Writeln)
        result_Println += COLOR["RED"]+ "Ssh Failure Site Fp may down " + "\n" + COLOR["ENDC"]
        print(result_Println)
        return
    
    SiteStatus_res = output
    #print(SiteStatus_res)
    result = split_string(SiteStatus_res, "]")
    ThermalValue = split_string(result[7],"[")
    #print(ThermalValue)
    DiodeTemp = split_string(ThermalValue[1]," ")
    #print(DiodeTemp)
       
    
    #
    try:
        command = "tsar GetSiteThermalStatusInternal"
        #output, error = ssh_command(hostname, username, password, command)
        output = "[23070010 0 0 0.004 0 NaN NaN [-0.001 -0.001 -0.001 -0.001] 12 0 0 0 NaN 19.301 12 0 0 0 100 NaN NaN NaN NaN NaN NaN 17.67 NaN NaN 512 0]"
        error = None
        if error:
            print("Error:")
            print(error)
            result_Writeln += " , Error : " + error 
            log_to_file(result_Writeln)
    except:
        #print("An exception occurred")
        result_Writeln += " , Ssh Failure Site Fp may down" 
        log_to_file(result_Writeln)
        result_Println += COLOR["RED"]+ "Ssh Failure Site Fp may down " + "\n" + COLOR["ENDC"]
        print(result_Println)
        return
       
    #print("Get Sitestatus InternalOutput:")
    #print(output)
    result = split_string(output, " ")
    CPThermalValue = result[16]
    #print(CPThermalValue)
    cpID = result[21]
    coolentValveValue = result[28]

    
    
    # Site Diode Temprature Check
    #print(DiodeTemp)
    for tempVal in DiodeTemp:
        
        if tempVal == 'NaN':
            #print(COLOR["PURPLE"], " - " , COLOR["ENDC"])
            result_Println += COLOR["LIGHTGRAY"]+ "NULL " + " | " + COLOR["ENDC"]
            result_Writeln += ",  " +" NULL "
        else :
            result_Writeln += ",  " + str(tempVal)
            num_float = float(tempVal.strip())  # Convert to float first
            diodeTemp_int = int(num_float)  # Convert to integer (truncates decimal)
            
            if diodeTemp_int > 70:
                result_Println += COLOR["RED"] + str(num_float) + " | " + COLOR["ENDC"]
            elif diodeTemp_int > 65:
                result_Println += COLOR["YELLOW"] + str(num_float) + " | " + COLOR["ENDC"]
            else :
                result_Println += COLOR["WHITE"] + str(num_float) + " | " + COLOR["ENDC"]
    
    
    # SiteThermalStatus Check 
    if CPThermalValue == 'NaN':
        result_Println += COLOR["LIGHTGRAY"]+ "NULL " + " | " + COLOR["ENDC"]
        result_Writeln += ",  " +" NULL "
    else :
        result_Writeln +=  ",   " + str(CPThermalValue) 
        num_float = float(CPThermalValue.strip())  # Convert to float first
        CPThermal_int = int(num_float)  # Convert to integer (truncates decimal)
        if int(CPThermal_int) > 70:
            result_Println += COLOR["RED"]+ str(num_float)+ " | " + COLOR["ENDC"]
        elif int(CPThermal_int) > 65:
            result_Println += COLOR["YELLOW"]+ str(num_float)+ " | " + COLOR["ENDC"]
        else :
            result_Println += COLOR["WHITE"]+ str(num_float)+ " | " + COLOR["ENDC"]
    
    # Cold Plate ID 
    if cpID == 'NaN':
        result_Println += COLOR["GREEN"]+ "NULL" + " | " + COLOR["ENDC"]
        result_Writeln += ",  " +"NULL"
    else :
        result_Writeln +=  ",   " + str(cpID) 
        result_Println += COLOR["GREEN"]+ str(cpID) + " | " + COLOR["ENDC"]

    
    # Cold plate Valve Valve Check 
    if coolentValveValue == 'NaN':
        result_Println += COLOR["LIGHTPURPLE"]+ "NULL" + " | " + COLOR["ENDC"]
        result_Writeln += ",  " +"NULL" + "\n"
    else :
        result_Writeln +=  ",   " + str(coolentValveValue) + "\n"
        result_Println += COLOR["CYAN"]+ str(coolentValveValue) + " | "+ COLOR["ENDC"]

    
    #Display on Screen
    print(result_Println)
    # wrire in to log
    log_to_file(result_Writeln)
    
    if error:
        print("Error:")
        print(error)
        
        
def askUser():
    while True:
        try:
            choice = int(input("Do you want : \n(1) 6 Pack Automation \n(2) 10 Pack Manual \n Enter your Option : "))
        except ValueError:
            print("Please input a number")
            continue
        if 0 < choice < 5:
            break
        else:
            print("\nThat is not between 1 and 2! Try again:")
    print ("\nYou entered: {} ".format(choice)) # Good to use format instead of string formatting with %
    
    #mydict[choice]()
    print(mydict[choice])
    return mydict[choice]


if __name__ == "__main__":
    
    # List of hostname
    hostNameList = ["192.168.1.1" ]
    #hostNameList = ["192.168.1.1" ,"192.168.1.2","192.168.1.3","192.168.1.4","192.168.1.5","192.168.1.6"]
    
    userChoice = askUser()
    print("User Choice :" + userChoice)
    if(mydict[2] == userChoice) is True :
        hostNameList = ["192.168.1.1" ,"192.168.1.2","192.168.1.3","192.168.1.4","192.168.1.5","192.168.1.6","192.168.1.7" ,"192.168.1.8","192.168.1.9","192.168.1.10"]
    
    print(hostNameList)
              
    
    # continuous Loop
    #while True:
    Header = COLOR["BLUE"]+ "Date and Time     :    Site IP    : Diode1   Diode2  Diode3  Diode4  CP_Thermal CP_ID CoolentValve_Value \n" + COLOR["ENDC"]  
    print(Header)
    for val in hostNameList:

        getSitetemprature(val)
        #except:
            #print("An exception occurred")
    print("3 Sec Delay")   
    #time.sleep(5) # Sleep for 5 seconds
    
        
    
        