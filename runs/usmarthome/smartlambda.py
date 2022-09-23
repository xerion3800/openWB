#!/usr/bin/python3
from usmarthome.smartbase import Sbase
from usmarthome.global0 import log
import subprocess


class Slambda(Sbase):
    def __init__(self):
        # setting
        super().__init__()
        print('__init__ Slambda executed')

    def getwatt(self, uberschuss, uberschussoffset):
        self.prewatt(uberschuss, uberschussoffset)
        argumentList = ['python3', self._prefixpy + 'lambda/watt.py',
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss), str(self.device_lambdaueb)]
        try:
            self.proc = subprocess.Popen(argumentList)
            self.proc.communicate()
            self.answer = self.readret()
            self.newwatt = int(self.answer['power'])
            self.newwattk = int(self.answer['powerc'])
            self.relais = int(self.answer['on'])
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('lambda', self.device_nummer,
                           str(self._device_ip), str(e1)))
        self.postwatt()

    def turndevicerelais(self, zustand, ueberschussberechnung, updatecnt):
        self.preturn(zustand, ueberschussberechnung, updatecnt)
        if (zustand == 1):
            pname = "/on.py"
        else:
            pname = "/off.py"
        argumentList = ['python3', self._prefixpy + 'lambda' + pname,
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss), str(self.device_lambdaueb)]
        try:
            self.proc = subprocess.Popen(argumentList)
            self.proc.communicate()
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") on / off  %s %d %s Fehlermeldung: %s "
                        % ('lambda', self.device_nummer,
                           str(self._device_ip), str(e1)))
