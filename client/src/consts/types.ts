export interface ITransfer{
    from:IPoint,
    to:IPoint
    duration: number,
    transport:string
    arrival:string,
    departure:string
}
export interface IPreTransfer{
    is_transfer:boolean
    route?:ITransfer
    details?:{
        from:string
        to:string
        duration:number
        transport_type:string
    }[]
}
export interface IInfoTransfer{
    info:IPreTransfer[],
    score:number
    duration:number,
    price:number
    id:number
    arrival:string
    departure:string
}
export interface IPoint{
    city_code:string,
    station_code:string,
    city_title:string
    station_title:string
}
