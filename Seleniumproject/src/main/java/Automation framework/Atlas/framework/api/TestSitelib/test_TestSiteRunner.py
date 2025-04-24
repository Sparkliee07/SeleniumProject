import json
import paramiko  # Ensure you have the paramiko package installed: pip install paramiko
import logging
import os
import time

class TSAR:
    def __init__(self, UserName, Password, IhcIP,FpIP,SiteIP, APIS):
        self.FpIP = FpIP
        self.IhcIP = IhcIP
        self.UserName = UserName
        self.Password = Password
        self.SiteIP = SiteIP
        self.APIS = APIS

class MRPCError(Exception):
    pass

def validate_tsar_commands():
    nResult = 0
    logging.info("*** Executing TSAR Commands ***")
    
    if os.path.exists("../../../tests/TestData\\TSAR.json"):
        logging.info(f"TSAR Json File found in the given path .\\TestData\\TSAR.json")
        with open("../../../tests/TestData\\TSAR.json", "r") as f:
            tsar_definitions = json.load(f)
        
        tsar = TSAR(tsar_definitions['UserName'], tsar_definitions['Password'],tsar_definitions['IHC_IP'],tsar_definitions['FpIP'],tsar_definitions['SiteIP'], tsar_definitions['APIS'])
        
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print(f"connecting SSh to  {tsar.IhcIP} ...")
            client.connect(tsar.IhcIP, username=tsar.UserName, password=tsar.Password)
            
            logging.info(f"SSHClient connection was successful for FP {tsar.IhcIP}")
            
                        
            for api in tsar.APIS:

                time.sleep(2)
                cmdPath = f"cd ../../teradyne/TestSiteRunner &&  ./TestSiteRunner {tsar.SiteIP} 1 {api['Name']} {' '.join(api['Parameters'])}"
                #cmdPath = f"tsar {api['Name']} {' '.join(api['Parameters'])}"
                logging.info(f"Full Command {cmdPath}")
                print(cmdPath)

                stdin, stdout, stderr = client.exec_command(cmdPath)
                reply = stdout.read().decode('utf-8').lower()
                logging.info(f"Output :",reply)
                print(reply)
                if any(error in reply for error in ["arguments mismatch", "could not parse", "exception", "api error", "invalid command", "not found", "not implemented"]):
                    logging.error(f"TSAR command {api['Name']} returned the reply with error: The method or operation is not implemented")
                    nResult = -1
                else:
                    logging.info(f"Reply from the API call {api['Name']} = {reply}")
            
        except Exception as e:
            logging.error(f"SSHClient connection was not successful for FP {tsar.IhcIP}")
        
    else:
        logging.error(f"TSAR Json File does not exist in the given path .\\TestData\\TSAR.json")
    
    remarks = "" if nResult >= 0 else "Fail in TSAR execution"
    return nResult, remarks


if __name__ == "__main__":
    result , remarks = validate_tsar_commands()   
