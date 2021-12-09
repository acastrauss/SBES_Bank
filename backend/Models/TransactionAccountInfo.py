# Define base account class info
# Define additional account FROM info
# Define additional account TO info

from TransactionClientInfo import TransactionClientInfo
from Shared.Enums.Currency import Currency

class TransactionAccountInfo():
    def __init__(
        self,
        accountNumber: str,
        clientInfo: TransactionClientInfo
    ) -> None:
        self.accountNumber = accountNumber
        self.clientInfo = clientInfo

class TransactionAccountFromInfo(
    TransactionAccountInfo
):
    def __init__(
        self,
        accountNumber: str,
        clientInfo: TransactionClientInfo,
        balanceBefore: float,
        balanceAfter: float,
        currency: Currency
        ) -> None:
        super().__init__(accountNumber, clientInfo)
        self.balanceBefore = balanceBefore
        self.balanceAfter = balanceAfter
        self.currency = currency

class TransactionAccountToInfo(
    TransactionAccountInfo
):
    def __init__(
        self,
        accountNumber: str, 
        clientInfo: TransactionClientInfo
        ) -> None:
        super().__init__(accountNumber, clientInfo)