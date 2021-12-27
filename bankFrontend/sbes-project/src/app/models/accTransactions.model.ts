import { PaymentCodeFKModel } from "./paymentCodeFK.model";
import { MyAccInfoFKModel } from "./myAccInfoFK.model";
import { TransferAccInfoFKModel } from "./transferAccInfoFK.model";
import { Data } from "@angular/router";
export interface AccTransactionsModel {
    id: number,
    amount: number,
    modelCode: number,
    paymentCodeFK: PaymentCodeFKModel,
    paymentPurpose: string,
    preciseTime: Data,
    provision: number,
    referenceNumber: number,
    transactionType: string,
    currency: string,
    myAccInfoFK: MyAccInfoFKModel,
    transferAccInfoFK: TransferAccInfoFKModel
}