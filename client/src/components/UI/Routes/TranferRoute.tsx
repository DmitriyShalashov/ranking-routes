import imgRoads from "../../../consts/img";
import { IPreTransfer, ITransfer } from "../../../consts/types"
import DirectRoute from "./DirectRoute";

function secondsToTime(seconds:number) {
    const hours = Math.floor(seconds / 3600); 
    const minutes = Math.floor((seconds % 3600) / 60); 
  
    const formattedHours = String(hours).padStart(2, "0");
    const formattedMinutes = String(minutes).padStart(2, "0");
    if(hours){
        return `${formattedHours} ч:${formattedMinutes} мин`;
    }
    else{
        return `${formattedMinutes} мин`;
    }
    
  }
  

function TransferRoute({routes}:{routes:IPreTransfer[]}){
    return (
    <div className="flex w-fit border-2 p-[5px] mb-[40px]">
        {
            routes.map((transfer)=>
                <div className="flex items-center justify-between">
                    {!transfer.is_transfer&&transfer.route
                        ?
                        <DirectRoute route={transfer.route}/>
                        :
                        <div className="w-[100px]">
                            <p className="text-[15px] mb-[10px] text-center">Пересадка</p>
                            <ul>
                                {transfer.details&&transfer.details.map((cross, index)=>
                                    <li className="text-[12px] h-fit justify-between flex items-center">
                                        <div className="flex flex-col items-center justify-between">
                                            {index!==0?<div className="w-[3px] h-[14px] bg-gray-900"></div>:<></>}
                                            <div className="rounded-[50%] w-[8px] h-[8px] border-gray-900 border-[2px] bg-white"></div>
                                            {index+1!==transfer.details?.length?<div className="w-[3px] h-[14px] bg-gray-900"></div>:<></>}
                                        </div>
                                        <img className="h-[22px]" src={imgRoads[`${cross.transport_type}`]} alt=""></img>
                                        <p className="">{secondsToTime(cross.duration)}</p>
                                    </li>
                                )}
                            </ul>
                        </div>
                    }
                    
                </div>
            )
        }
        </div>
    )
}

export default TransferRoute