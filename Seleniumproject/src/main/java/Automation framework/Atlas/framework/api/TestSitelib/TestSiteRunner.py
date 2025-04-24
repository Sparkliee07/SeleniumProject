import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from operator import truediv

import paramiko  # Ensure you have the paramiko package installed: pip install paramiko
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -----------------------------
#       TSAR class
# -----------------------------
class TSAR:
    def __init__(self, UserName, Password, IhcIP, FpIP, SiteIP,SlotNo):
        self.FpIP = FpIP
        self.IhcIP = IhcIP
        self.UserName = UserName
        self.Password = Password
        self.SiteIP = SiteIP
        self.SlotNo = SlotNo
        self.SSH_Client = paramiko.SSHClient()



    def ConnectSsh(self):
        logging.info(f"*** Connecting SSH to {self.IhcIP} ...  ***")
        try:
            self.SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.SSH_Client.connect(self.IhcIP, username=self.UserName, password=self.Password)
            logging.info(f"SSHClient connection was successful for FP {self.IhcIP}")
            return True
        except Exception as e:
            logging.error(f"SSHClient connection was not successful for FP {self.IhcIP}")
        return False


    def disconnectSsh(self):
        # tsar.SSH_Client.d
        # Disconnect the SSH client
        self.SSH_Client.close()
        print("SSH client disconnected")


    def executeSsh_Command(self, apiName, fullCMD):

        logging.info(f"TSAR Command {fullCMD}")
        cmdHeader = f"cd ../../teradyne/TestSiteRunner && ./TestSiteRunner {self.SiteIP} {self.SlotNo} "
        fullCMD = cmdHeader + fullCMD
        stdin, stdout, stderr = self.SSH_Client.exec_command(fullCMD)
        reply = stdout.read().decode('utf-8').lower()
        if any(error in reply for error in
               ["arguments mismatch", "could not parse", "exception", "api error", "invalid command", "not found",
                "not implemented"]):
            logging.error(
                f"TSAR command {apiName} returned the reply with error: The method or operation is not implemented Reply = {reply}")

            return False,reply
        else:
            logging.info(f"Response for the API call {apiName} : {reply}")
            return True,reply


def validate_tsar_commands():
    # logger.info(tsar_definitions)
    #tsar = TSAR()
    tsar = TSAR(UserName="cpc", Password="Teradyne", IhcIP="131.101.47.35", FpIP="192.168.122.1",
                SiteIP="192.168.122.1",SlotNo=1)

    tsar.ConnectSsh()
    tsar.executeSsh_Command( "GetMfgInfo", f"GetMfgInfo")
    tsar.disconnectSsh()

    return

if __name__ == "__main__":
    # Log the message
    validate_tsar_commands()



