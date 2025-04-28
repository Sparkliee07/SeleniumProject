import sys
import os
import logging
import paramiko

class TSAR:
    def __init__(self):
        # logger.info(tsar_definitions)
        self.TSAR_FileName = "TSAR_Config.json"
        self.FpIP = None
        self.IhcIP = "131.101.47.35"
        self.UserName = "cpc"
        self.Password = "Teradyne"
        self.SiteIP = "192.168.122.1"
        self.SlotNo = 1
        self.APIS = None
        #self.GetTSAR_JsonDataConnectSsh()
        self.SSH_Client = paramiko.SSHClient()



    def ConnectSsh(self):
        logging.info(f"*** Connecting SSH to {self.IhcIP} ...  ***")
        try:
            self.SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.SSH_Client.connect(self.IhcIP, username=self.UserName, password=self.Password)
            logging.info(f"SSHClient connection was successful for {self.IhcIP}")
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
        nResult = True
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
            nResult = False
            return nResult,reply
        else:
            logging.info(f"Response for the API call {apiName} : {reply}")
            return nResult,reply


Embedd_featues = ["Get Manufacturing Info"]

def before_all(context):
    """Executed once before all tests"""
    print("\n[HOOK] Before all scenarios")
    os.environ["ALLURE_REPORT_TITLE"] = "Atlas Titan Hp Report "
    context.test_data = {}



def before_feature(context, feature):
    """Executed before each feature"""
    print(f"\n[HOOK] Before feature: {feature.name}")
    feature_name = context.feature.name
    if feature_name in Embedd_featues:
        print(f"\n[HOOK] Before scenario - Setting up TestSiteRunner for {feature_name} ")
        context.tsar = TSAR()
        #context.ConnectSsh()
        context.base_url = ""
    elif feature_name == "Sample Feature":
        print("\n[HOOK] Before scenario - Setting up Sample Feature")
        context.base_url = ""

    elif feature_name == "Search Feature":
        print("\n[HOOK] Before scenario - Setting up Search Feature")
        context.base_url = ""

    else:
        print(f"\n[HOOK] Before scenario - Default setup for {feature_name}")



def before_step(context, step):
    """Executed before each step"""
    #print(f"\n[HOOK - Before step] Before step: {step.name}")



def after_step(context, step):
    """Executed after each step"""
    #print(f"[HOOK -  After step] After step: {step.name}")
    #sys.stdout.flush()  # Ensure print statements are displayed immediately


def after_scenario(context, scenario):
    """Executed after each scenario"""
    print(f"[HOOK] After scenario: {scenario.name}")


def after_feature(context, feature):
    """Executed after each feature"""
    print(f"[HOOK] After feature: {feature.name}")


def after_all(context):
    """Executed once after all tests"""
    print("\n[HOOK] After all scenarios")
