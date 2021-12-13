export interface CardModel{
    cardHolder : string,
    cardNumber: string,
    cardType : CardType,
    cvc : number,            
    pin : number,
    validUntil : Date,
    processor : CreditCardProcessor
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