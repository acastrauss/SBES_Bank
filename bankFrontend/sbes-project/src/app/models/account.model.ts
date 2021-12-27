import { ClientModel } from "./client.model";

export interface AccountModel{
   accountBalance : number,
   accountNumber : string,
   blocked : boolean,
   clientId : ClientModel,
   currency : string,
   dateCreated : Date,
   id : number
}

enum Currency{
    USD,
    EUR,
    CHF,
    GBP,
    RUB,
    CAD,
    AUD,
    RSD,
    DKK,
    SEK,
    NOK,
    JPY
}