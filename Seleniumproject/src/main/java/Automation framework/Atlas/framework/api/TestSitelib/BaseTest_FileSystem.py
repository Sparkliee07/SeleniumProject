import os
import shutil
import gzip
import re
from xml.etree import ElementTree as ET
from ATLAS.framework.api.TestSiteLib.TestStatus import TestStatus


class BaseTest:
    def LogResult(self, status, *args):
        # Placeholder for logging method
        print(f"Status: {status}, Details: {args}")

    def CreateDir(self, path):
        status = TestStatus.Pass
        error = None
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as ex:
            status = TestStatus.FAIL
            error = str(ex)
        self.LogResult(status, "Create directory", "Path:", path)
        if error:
            self.LogResult(status, "Create directory", "Error:", error)

    def RemoveDir(self, path):
        status = TestStatus.Pass
        error = None
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
        except Exception as ex:
            status = TestStatus.FAIL
            error = str(ex)
        self.LogResult(status, "Remove directory", "Path:", path)
        if error:
            self.LogResult(status, "Remove directory", "Error:", error)

    def CopyDir(self, source, dest):
        status = TestStatus.Pass
        error = None
        try:
            shutil.copytree(source, dest)
        except Exception as ex:
            status = TestStatus.FAIL
            error = str(ex)
        self.LogResult(status, "Copy directory", "From:", source, "To:", dest)
        if error:
            self.LogResult(status, "Copy directory", "Error:", error)

    def CopyFile(self, source, dest):
        status = TestStatus.Pass
        error = None
        try:
            shutil.copy2(source, dest)
        except Exception as ex:
            status = TestStatus.FAIL
            error = str(ex)
        self.LogResult(status, "Copy file", "From:", source, "To:", dest)
        if error:
            self.LogResult(status, "Copy file", "Error:", error)

    def DeleteFile(self, path):
        status = TestStatus.Pass
        error = None
        try:
            os.remove(path)
        except Exception as ex:
            status = TestStatus.FAIL
            error = str(ex)
        self.LogResult(status, "Delete file", "Path:", path)
        if error:
            self.LogResult(status, "Delete file", "Error:", error)

    def GUnzip(self, filename):
        with gzip.open(filename, 'rb') as in_stream:
            with open(os.path.splitext(filename)[0], 'wb') as out_stream:
                shutil.copyfileobj(in_stream, out_stream)

    def ReadXml(self, filename, readSettings=None, loadOptions=None, *replacements):
        # Read the file.
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()

        # Make replacements.
        for i in range(0, len(replacements), 2):
            pattern = replacements[i]
            replacement = replacements[i + 1]
            text = re.sub(pattern, replacement, text)

        # Parse the XML.
        return ET.ElementTree(ET.fromstring(text))

if __name__ == "__main__":
    # Example usage of the class methods
    base_test = BaseTest()
    base_test.CreateDir('test_dir')
    base_test.RemoveDir('test_dir')
    base_test.CopyFile('source.txt', 'dest.txt')
    base_test.DeleteFile('dest.txt')
    base_test.GUnzip('file.gz')
    xml_tree = base_test.ReadXml('file.xml', replacements=('pattern1', 'replacement1', 'pattern2', 'replacement2'))