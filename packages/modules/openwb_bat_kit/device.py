import logging
from typing import Dict, Optional, List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext
from modules.openwb_bat_kit import bat
from modules.common import modbus
from modules.common.fault_state import FaultState

log = logging.getLogger(__name__)


def get_default_config() -> dict:
    return {
        "name": "OpenWB Speicher-Kit",
        "type": "openwb_bat_kit",
        "id": 0,
        "configuration": {
            "version": 2
        }
    }


class Device(AbstractDevice):
    def __init__(self, device_config: dict) -> None:
        self.device_config = device_config
        self._components = {}  # type: Dict[str, bat.BatKit]
        version = self.device_config["configuration"]["version"]
        if version == 0 or version == 1:
            ip_address = '192.168.193.19'
        elif version == 2:
            ip_address = '192.168.193.15'
        else:
            raise FaultState.error("Version " + str(version) + " unbekannt.")
        self.client = modbus.ModbusClient(ip_address, 8899)

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type == "bat":
            self._components["component"+str(component_config["id"])] = bat.BatKit(
                self.device_config, component_config, self.client)
        else:
            raise Exception(
                "illegal component type " + component_type)

    def update(self) -> None:
        log.debug("Start device reading " + str(self._components))
        if self._components:
            for component in self._components:
                # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(self._components[component].component_info):
                    self._components[component].update()
        else:
            log.warning(
                self.device_config["name"] +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


def read_legacy(component_type: str, version: int, num: Optional[int] = None, evu_version: Optional[int] = None):
    """ Ausführung des Moduls als Python-Skript
    """

    device_config = get_default_config()
    dev = Device(device_config)

    component_config = get_component_config(component_type, version, num)
    dev.add_component(component_config)
    log.debug('openWB Version: ' + str(version))

    if component_type == "evu_inverter" and evu_version:
        component_config = get_component_config("counter", evu_version, None)
        dev.add_component(component_config)
        log.debug('openWB EVU-Version: ' + str(evu_version))

    dev.update()


def get_component_config(component_type: str, version: int, num: Optional[int] = None) -> Dict:
    if component_type == "bat":
        component_config = bat.get_default_config()
    else:
        raise Exception("illegal component type " + component_type)
    component_config["id"] = num
    component_config["configuration"]["version"] = version
    return component_config


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
