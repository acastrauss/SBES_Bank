export interface AccountModel{
   accountBalance : number,
   accountNumber : string,
   blocked : boolean,
   currency : Currency,
   dataCreated : Date,
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