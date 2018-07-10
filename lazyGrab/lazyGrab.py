#!/usr/bin/env python3

import os
import sys
import platform
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
except ImportError:
    sys.stderr.write("Please install selenium with 'pip install -U selenium'.\n\n")
    sys.exit(-1)
try:
    from slugify import slugify
except ImportError:
    sys.stderr.write("Please install slugify with 'pip install python-slugify'.\n\n")
    sys.exit(-1)


class Shooter():
    def __init__(self, targets_list, verbose=False, validate_certificates=False):
        self.platform_name = platform.system()
        self.cert_validation = validate_certificates
        self.binary_path = "%s/selenium_binaries/chromedriver_%s" % (
                                                    os.getcwd(),
                                                    self.platform_name.lower()
                                                    )
        if not os.path.exists(self.binary_path):
            sys.stderr.write("[!]\tCould not find chromedrivers binaries.\n")
            sys.stderr.write("[!]\tExiting now. Please check this path:\n")
            sys.stderr.write("[!]\t\t%s\n\n"%self.binary_path)
            sys.exit(-1)
        self._loadSelenium()

        if not os.path.exists(targets_list):
            sys.stderr.write("[!]\tCould not find the target file.\n")
            sys.stderr.write("[!]\tExiting now. Please check this path:\n")
            sys.stderr.write("[!]\t\t%s\n\n"%targets_list)
            sys.exit(-1)

        self.targetsFilePath = targets_list
        self._loadAndParseTargetsFile()
        self.OutputDirectory = "products"
        self.verbose = verbose

    """ Load target bank """
    def _loadAndParseTargetsFile(self):
        retMe = []
        try:
            f = open(self.targetsFilePath, 'r')
        except IOError as e:
            sys.stderr.write("[!]\tError opening file '%s'.\n" % self.targetsFilePath)
            sys.stderr.write("[!]\t%s.\n" % str(e))
            sys.exit(-1)
        lines = f.readlines()
        f.close()
        for line in lines:
            tar = line.strip()
            if tar is None or tar is "":
                continue
            retMe.append(tar)
        sys.stdout.write("[.]\t%s targets loaded from file.\n" % len(retMe))
        self.Targets = retMe
        return True

    """ Loads the selenium object in headless mode """
    def _loadSelenium(self):
        chrome_options = Options()
        if not self.cert_validation:
            chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--test-type")
        self.driver = webdriver.Chrome(
                                chrome_options=chrome_options,
                                executable_path=self.binary_path
                                )
        sys.stdout.write("[+]\tSelenium loaded with chromedriver.\n")

    """ Do the Snap """
    def _snap(self, target):
        try:
            self.driver.get(target)
        except:
            return False

        if "Unauthorized" in self.driver.page_source:
            pass
        elif self.driver.title == "" or self.driver.title == None:
            return False

        if self.verbose:
            if target != self.driver.current_url[:-1]:
                sys.stdout.write("[.]\tSite '%s' redirected to '%s'.\n" % (target, self.driver.current_url))

        fname = "%s/%s_%s.png" % (self.OutputDirectory, slugify(target), slugify(self.driver.current_url))
        self.driver.get_screenshot_as_file(fname)
        return True

    """ Take a snapshot """
    def ShootIt(self, address):
        if "http://" in address or "https://" in address:
            if self._snap(target=address):
                if self.verbose:
                    sys.stdout.write("[+]\t'%s' was found.\n" % address)
                    return False
            else:
                if self.verbose:
                    sys.stderr.write("[-]\tCould not get '%s'.\n" % address)
                    return False


        # No http/https was requested.
        thisTarget = "http://%s" % address
        if self._snap(target=thisTarget):
            if self.verbose:
                sys.stdout.write("[+]\t'%s' was found.\n" % thisTarget)
        else:
            if self.verbose:
                sys.stderr.write("[-]\tCould not get '%s'.\n" % thisTarget)
        thisTarget = "https://%s" % address
        if self._snap(target=thisTarget):
            if self.verbose:
                sys.stdout.write("[+]\t'%s' was found.\n" % thisTarget)
        else:
            if self.verbose:
                sys.stderr.write("[-]\tCould not get '%s'.\n" % thisTarget)
        return True

    """ Take a snapshot from all targets """
    def Run(self):
        sys.stdout.write("[.]\tStarting loop execution on %s targets.\n" % len(self.Targets))
        for target in self.Targets:
            self.ShootIt(address=target)
        sys.stdout.write("[.]\tCompleted execution on %s targets.\n" % len(self.Targets))

    """ Maid cleanup service """
    def Close(self):
        self.driver.close()
        sys.stdout.write("[+]\tCleanup completed.\n\n")


def main():
    if len(sys.argv) <  2:
        TARGETNAME = 'demo_ips.txt'
        sys.stdout.write("[.]\tYou gave me no parameters so i'm assuming target bank is 'demo_ips.txt'.\n")
    else:
        TARGETNAME = sys.argv[1]

    a = Shooter(targets_list=TARGETNAME)
    a.Run()
    a.Close()


if __name__ == "__main__":
    main()
