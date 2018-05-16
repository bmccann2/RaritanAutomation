'''
Created on May 26, 2016
@author: brendanm
Description: KX3-2685 Network Statistics_S
TestLink Folder: Raritan-Diagnostics-Network Stats
Identifier: DFTC003
Status: Complete
'''

import traceback
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from SeleniumPython.KVM.KX3.Utilities import Login, FileSetup, DriverControl as DC
from SeleniumPython.KVM.KX3.PageObjects.Diagnostics import DiagnosticsMenu, NetworkStatistics


class Test2685(unittest.TestCase):
        
    def test_main(self):
        ResultFile=FileSetup.results
        text=['Ip:', 'IPv6', 'Kernel Interface table', 'connections']
        options=['--statistics', '--route', '--interfaces','--ports']    
        driver=DC.setUpFireFox(self, Login.IP)
        identifier= 'DFTC003 Network Statistics'
        ''' Step 1: Power On KX'''

        wait = WebDriverWait(driver, 5)
        
        try:
            Login.login(self, driver, wait)
            '''Step 2: Login from HTML client'''
            
            DiagnosticsMenu.NetworkStatistics(self, driver, wait)
            '''Step 3: Select Diagnostics/Network Statisctics'''
                    
            wait.until(EC.frame_to_be_available_and_switch_to_it('container'))
            assert NetworkStatistics.getCrrntSelbx_Option(self, driver, wait)=='statistics'
            '''Step 4: Verify that "statistics" is the default option in dropdown list and reported in results field'''
            
            for x in range(0, len(text)):
                NetworkStatistics.clickBtn_Refresh(self, driver, wait)
                wait.until(EC.presence_of_element_located((By.XPATH, "//table[@class='tmpl_tab']/tbody/tr[5]/td/div/br")))
                assert text[x] in driver.page_source
                if x!=3:
                    NetworkStatistics.setSelbx_Option(self, driver, wait, options[x+1])
                    assert text[x] in driver.page_source
                    '''Potential to be changed'''
            '''Steps 5-10: pick each of the options and hit refresh'''
                    
            Login.logout(self, driver, wait)
            ResultFile.write(identifier+', Passed, ('+FileSetup.date+' '+FileSetup.time+')\n')
            
        except:
            ErrorLog= FileSetup.errorReport()
            ResultFile.write(identifier+', Failed, ('+FileSetup.date+' '+FileSetup.time+')\n')
            ErrorLog.write(identifier+', Failed, ('+FileSetup.date+' '+FileSetup.time+' '+traceback.format_exc(1, True)+')\n')    
    
            
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
    
