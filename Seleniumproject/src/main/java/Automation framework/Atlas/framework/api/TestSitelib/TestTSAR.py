import json
import paramiko  # Ensure you have the paramiko package installed: pip install paramiko
import logging
import os

class TSAR:
    def __init__(self, FpIP, UserName, Password, SiteIP):
        self.FpIP = FpIP
        self.UserName = UserName
        self.Password = Password
        self.SiteIP = SiteIP


class MRPCError(Exception):
    pass

def validate_tsar_commands():
    logging.info("*** Executing TSAR Commands ***")
    
    if os.path.exists("../../../Config/TSAR_Config.json"):
        logging.info(f"TSAR Json File found in the given path .\\TestData\\TSAR.json")
        with open("../../../Config/TSAR_Config.json", "r") as f:
            tsar_definitions = json.load(f)
        
        print(tsar_definitions['FpIP'])
        tsar = TSAR(tsar_definitions['FpIP'], tsar_definitions['UserName'], tsar_definitions['Password'], tsar_definitions['SiteIP'])
        
        try:

            IHC_IP="131.101.47.35"
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(tsar.FpIP, username=tsar.UserName, password=tsar.Password)

            
            logging.info(f"SSHClient connection was successful for FP {IHC_IP}")
            
                        
            for api in tsar.APIS:
                print(api)
                time.sleep(2)
                #cmdPath = f"cd C:\\Teradyne\\Atlas\\TitanHP\\Bin\\TestSiteRunner {tsar.SiteIP} 1 {api['Name']} {' '.join(api['Parameters'])}"
                arg = ' '.join(api['Parameters'])
                
                print(arg)
                cmdPath = f"tsar {api['Name']} {' '.join(api['Parameters'])}"
                logging.info(f"Full Command {cmdPath}")
                print(cmdPath)

                stdin, stdout, stderr = client.exec_command(cmdPath)
                reply = stdout.read().decode('utf-8').lower()
                logging.info(f"Output :",reply)
                if any(error in reply for error in ["arguments mismatch", "could not parse", "exception", "api error", "invalid command", "not found", "not implemented"]):
                    logging.error(f"TSAR command {api['Name']} returned the reply with error: The method or operation is not implemented")
                    nResult = -1
                else:
                    logging.info(f"Reply from the API call {api['Name']} = {reply}")
            
        except Exception as e:
            logging.error(f"SSHClient connection was not successful for FP {tsar.FpIP}")
        
    else:
        logging.error(f"TSAR Json File does not exist in the given path .\\TestData\\TSAR.json")
    
    remarks = "" if nResult >= 0 else "Fail in TSAR execution"
    return nResult, remarks


if __name__ == "__main__":
    result , remarks = validate_tsar_commands()   
