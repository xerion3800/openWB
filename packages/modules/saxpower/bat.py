#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.simcount import SimCounter
from modules.common.store import get_bat_value_store
from modules.saxpower.config import SaxpowerBatSetup


class SaxpowerBat:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SaxpowerBatSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(SaxpowerBatSetup, component_config)
        self.__tcp_client = tcp_client
        self.__sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="speicher")
        self.__store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        with self.__tcp_client:
            # Die beiden Register müssen zwingend zusammen ausgelesen werden, sonst scheitert die zweite Abfrage.
            soc, power = self.__tcp_client.read_holding_registers(46, [ModbusDataType.INT_16]*2, unit=64)
            power = power * -1

        imported, exported = self.__sim_counter.sim_count(power)
        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.__store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=SaxpowerBatSetup)
