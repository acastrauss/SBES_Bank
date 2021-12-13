export interface TransactionModel{
    id : string,
    amount: number,
    modelCode : number,
    paymentCoDE : {[key : number] : string},            //dictinaory
    paymentPurpose : string,
    preciseTime : Date,
    provision : number,
    referenceNumber : string,
    accountFrom : string,
    accountTo : string,
    succesful : boolean
}