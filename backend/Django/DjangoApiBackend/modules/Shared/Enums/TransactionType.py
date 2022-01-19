from enum import Enum


class TransactionType(Enum):
    INFLOW = 0
    OUTFLOW = 1

    def __str__(self) -> str:
        return str(self.value)

    def __int__(self) -> int:
        return int(self.value)

    def GetFromStr(value:str):
        if(value.strip().upper() == "INFLOW"):
            return TransactionType.INFLOW
        else:
            return TransactionType.OUTFLOW