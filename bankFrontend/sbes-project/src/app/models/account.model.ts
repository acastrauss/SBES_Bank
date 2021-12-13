export interface AccountModel{
   accountBalance : number,
   accountNumber : number,
   blocked : boolean,
   currency : Currency,
   dataCreated : Date,
   maintenanceCost : number
}

enum Currency{
    USD,
    EUR,
    CHF,
    GBR,
    RUB,
    CNY,
    CAD,
    AUD,
    RSD
}