import paramiko
import os
import json


class TSAR:
    def __init__(self, FpIP, UserName, Password, SiteIP, APIS):
        self.FpIP = FpIP
        self.UserName = UserName
        self.Password = Password
        self.SiteIP = SiteIP
        self.APIS = APIS
        self.hostname = ""
        self.client = paramiko.SSHClient()
        


    def execute_Cmd(self,full_command):

        print(' ')
        stdin, stdout, stderr = self.client.exec_command(full_command)
        print("Output:", stdout.read().decode('utf-8'))
        print("Error:", stderr.read().decode('utf-8'))
        print('-----------------------------------------')


    def ssh_connect(self,hostname):
        print("hostname ",hostname,"FP :", tsar.FpIP,"SiteIP",tsar.SiteIP)
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())    
        self.client.connect(hostname, username=tsar.UserName, password=tsar.Password)
        print(f"SSHClient connection was successful for FP {hostname}")
    

    def ssh_disconnect(self):
        self.client.close()


    def ExecuteAll_API(self):
       
        for api in self.APIS:
            #cmdPath = f"./TestSiteRunner {hostname} 1 {api['Name']} {' '.join(api['Parameters'])}"
            full_command = f"tsar {api['Name']} {' '.join(api['Parameters'])}"
            print(full_command)
            #self.execute_Cmd(full_command)

        


# Example usage
if os.path.exists("../../../tests/TestData\\TSAR.json"):
    print(f"TSAR Json File found in the given path .\\TestData\\TSAR.json")
    with open("../../../tests/TestData\\TSAR.json", "r") as f:
        tsar_definitions = json.load(f)
        
# create the object for the TSAR Class    
tsar = TSAR(tsar_definitions['FpIP'], tsar_definitions['UserName'], tsar_definitions['Password'], tsar_definitions['SiteIP'], tsar_definitions['APIS'])

tsar.ssh_connect(tsar.FpIP)


# execute on ssh
try:
    # change the ssh current directory to ../../teradyne/TestSiteRunner'
    directory = '../../teradyne/TestSiteRunner'
    full_command = f"cd {directory}"
    tsar.execute_Cmd(full_command)
    tsar.execute_Cmd('ls -l')
    # iterate the commands one by one and verify the results
    for api in tsar.APIS:
        #command = f"./TestSiteRunner {tsar.FpIP} 1 {api['Name']} {' '.join(api['Parameters'])}"
        print()
        full_command = f'./TestSiteRunner 192.168.1.9 1 Getsiteinfo'
        #full_command = f"tsar {api['Name']} {' '.join(api['Parameters'])}"
        print()
        print(full_command)
        tsar.execute_Cmd(full_command)


except Exception as e:
    print(f"An error occurred: {e}")

tsar.ssh_disconnect()


