#!/usr/bin/env python3

from typing import Dict

from helpermodules import log
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store


def get_default_config() -> dict:
    return {
        "name": "BatterX Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration": {}
    }


class BatterXInverter:
    def __init__(self, device_id: int, component_config: dict) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, resp: Dict) -> None:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")

        power = resp["1634"]["0"] * -1

        topic = "openWB/set/system/device/" + str(self.__device_id)+"/component/" + str(self.component_config["id"])+"/"
        _, counter = self.__sim_count.sim_count(power, topic=topic, data=self.__simulation, prefix="pv")

        inverter_state = InverterState(
            power=power,
            counter=counter
        )
        self.__store.set(inverter_state)
