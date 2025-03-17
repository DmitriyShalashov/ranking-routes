import imgRoads from "../../../consts/img"
import { ITransfer } from "../../../consts/types"

const formattedMonth:{[key:number]:string}={
    1:"янв",
    2:"фев",
    3:"мар",
    4:"апр",
    5:"мая",
    6:"июня",
    7:"июля",
    8:"авг",
    9:"сен",
    10:"окт",
    11:"ноя",
    12:"дек",
}
const daysOfWeek = ["вс", "пн", "вт", "ср", "чт", "пт", "сб"];

function secondsToHoursMinutes(seconds:number) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
  
    const formattedHours = String(hours).padStart(2, "0");
    const formattedMinutes = String(minutes).padStart(2, "0");
  
    return `${formattedHours}ч:${formattedMinutes}мин`;
  }
  
function dateFromDateTime(dateString:string){
    const date = new Date(dateString);
    const day = date.getDate(); 
    const month = date.getMonth() + 1;
    const hours = date.getHours(); 
    const minutes = date.getMinutes();
    const dayOfWeek = daysOfWeek[date.getUTCDay()];
    const formattedDay = String(day).padStart(2, '0');  
    const formattedHours = String(hours).padStart(2, '0'); 
    const formattedMinutes = String(minutes).padStart(2, '0'); 

    return [ `${formattedDay} ${formattedMonth[month]}, ${dayOfWeek}`, `${formattedHours}:${formattedMinutes}`];
}  

function DirectRoute({route}:{route:ITransfer}){
    return (
        
        <div className="w-[250px] mt-[10px] mx-[30px] p-[5px]">
            <div className="flex gap-[20px]">
                <div>
                    <div className="h-[20px] w-[20px] rounded-[50%] border-[4px] border-[#F37022]"></div>
                    <div className="w-[4px] ml-[8px] h-[200px] bg-[#F37022] "></div>
                    <div className="h-[20px] w-[20px] rounded-[50%] border-[4px] border-[#F37022]"></div>
                </div>
                <div className="flex h-[260px]  flex-col justify-between">
                    <div>
                        <h1 className="text-[20px] leading-none">{dateFromDateTime(route.departure)[1]}</h1>
                        <p className="text-[12px] text-gray-500">{dateFromDateTime(route.departure)[0]}</p>
                    </div>
                    <p className="text-[14px] text-gray-500">{secondsToHoursMinutes(route.duration)}</p>
                    <div>
                        <h1 className="text-[20px] leading-none">{dateFromDateTime(route.arrival)[1]}</h1>
                        <p className="text-[12px] text-gray-500">{dateFromDateTime(route.arrival)[0]}</p>
                    </div>
                </div>
                <div className="flex  h-[260px] ml-[20px] flex-col justify-between">
                    <div>
                        <h1 className="text-[20px] leading-none">{route.from.city_title}</h1>
                        <p className="text-[12px] text-gray-500">{route.from.station_title}</p>
                    </div>
                    {route &&<img className="w-[40px] h-[40px]" src={imgRoads[`${route.transport}`]} alt=""></img>}
                    <div>
                        <h1 className="text-[20px] leading-none">{route.to.city_title}</h1>
                        <p className="text-[12px] text-gray-500">{route.to.station_title}</p>
                    </div>
                </div>
            </div>
        </div>

    )
}

export default DirectRoute