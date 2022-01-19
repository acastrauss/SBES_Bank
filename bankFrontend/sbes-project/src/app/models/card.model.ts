export interface CardModel{
    id:number,
    cardHolder : string,
    cardNumber: string,
    cvc : string,            
    pin : string,
    cardType : CardType,
    validUntil : Date,
    cardProcessor : CreditCardProcessor,
    key : string
}
enum CardType {
    DEBIT,
    CREDIT
}

enum CreditCardProcessor {
    VISA,
    MASTER_CARD,
    AMERICAN_EXPRESS
}