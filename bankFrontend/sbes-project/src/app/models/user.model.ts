export interface UserModel {
    billingAddress : string,
    birthDate : Date,
    email : string,
    fullName : string,
    gender : Gender,
    id : number,
    jmbg : number,
    password : string,
    username : string,
    userType:string
}

enum Gender { 
    MALE,
    FEMALE
}

