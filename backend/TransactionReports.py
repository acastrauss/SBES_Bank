
class ITransactionReport:
    def WriteReportText(transaction: Transaction):
        pass

    def WriteReportToFile(transaction: Transaction):
        pass


class CSVTransactionReport(ITransactionReport):
    def WriteReportText(transaction: Transaction):
        return f"""
            Id:{transaction.}
        """

    def WriteReportToFile(transaction: Transaction):
        pass

from Transaction import Transaction