import { useEffect, useState } from "react";
import { IInfoTransfer, IPreTransfer, ITransfer } from "../../../consts/types"
import { useGetTransfersMutation } from "../../../store/api/TransferApi"
import TransferRoute from "./TranferRoute";
import DirectRoute from "./DirectRoute";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../../store";
import { setIsSearchClicked, setSearchQuery } from "../../../store/slices/SearchSlice";
import { ClipLoader, RingLoader } from "react-spinners";
import imgRoads from "../../../consts/img";


function RouteList(){
    const sortingDuration=()=>{
      const newRoutes=routes.sort((a,b)=>a["duration"]-b["duration"])
      setRoutes([...newRoutes])
    }
    const sortingScore=()=>{
      const newRoutes=routes.sort((a,b)=>b["score"]-a["score"])
      setRoutes([...newRoutes])
    }
    const sortingPrice=()=>{
      const newRoutes=routes.sort((a,b)=>a["price"]-b["price"])
      setRoutes([...newRoutes])
    } 
    const sortingArr=()=>{
      const newRoutes=routes.sort((a,b)=>new Date(a.arrival).getTime()-new Date(b.arrival).getTime())
      setRoutes([...newRoutes])
    }
    const sortingDep=()=>{
      const newRoutes=routes.sort((a,b)=>new Date(a.departure).getTime()-new Date(b.departure).getTime())
      setRoutes([...newRoutes])
    }



    const [routes, setRoutes]=useState([] as IInfoTransfer[])

    const searchQuery=useSelector((state:RootState)=>state.search)
    const geo=useSelector((state:RootState)=>state.geo)
    const [isLoading, setLoading]=useState(true)
    const [isFetching, setIsFetching]=useState(false)

    const dispatch=useDispatch()
    const [getTransfers] = useGetTransfersMutation()
    useEffect(() => {
      if(!searchQuery.isSearchClicked){

      }
      else if(!geo.frm || !geo.to || !searchQuery.searchQuery.date){
        alert("Вы не ввели параметр")
      }
      else{
        setIsFetching(true)
        setLoading(true)
        getTransfers({
          frm:geo.frm,
          to:geo.to,
          date:searchQuery.searchQuery.date,
          transfers:true
        }).then(({data})=>{
          let sortedData=[] as IInfoTransfer[]
          sortedData=data&&JSON.parse(data).data.sort((a:IInfoTransfer,b:IInfoTransfer)=>b["score"]-a["score"])
          setRoutes(sortedData)
          console.log(data)
          setLoading(false)
          setIsFetching(false)
        })
        .catch((e)=>console.log(searchQuery.searchQuery.date))
        
      }    
      dispatch(setIsSearchClicked(false))
    },[searchQuery.isSearchClicked])

    function secondsToHoursMinutes(seconds:number) {
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
    
      const formattedHours = String(hours).padStart(2, "0");
      const formattedMinutes = String(minutes).padStart(2, "0");
    
      return `${formattedHours}ч:${formattedMinutes}мин`;
    }


    return (
        <div className="mt-[100px] ml-auto">
          <div className="flex justify-between mb-[40px] items-center">
            <div className="flex gap-[25px] h-[40px]"> 
              <button className="hover:bg-orange-600 shadow-xl hover:shadow-2xl px-[8px] py-[7px] text-white bg-[#F37022] rounded-[10px]" onClick={()=>sortingPrice()}>По цене</button>
              <button className="hover:bg-orange-600 shadow-xl hover:shadow-2xl px-[8px] py-[7px] text-white bg-[#F37022] rounded-[10px]" onClick={()=>sortingDuration()}>По длительности</button>
              <button className="hover:bg-orange-600 shadow-xl hover:shadow-2xl px-[8px] py-[7px] text-white bg-[#F37022] rounded-[10px]" onClick={()=>sortingScore()}>Рекомендованные</button>
              <button className="hover:bg-orange-600 shadow-xl hover:shadow-2xl px-[8px] py-[7px] text-white bg-[#F37022] rounded-[10px]" onClick={()=>sortingArr()}>По прибытию</button>
              <button className="hover:bg-orange-600 shadow-xl hover:shadow-2xl px-[8px] py-[7px] text-white bg-[#F37022] rounded-[10px]" onClick={()=>sortingDep()}>По отправлению</button>
            </div>
            <div className="flex gap-[25px] items-center"> 
              <img className="cursor-pointer h-[60px]" src={imgRoads["train"]} alt=""></img>
              <img className="cursor-pointer h-[60px]" src={imgRoads["plane"]} alt=""></img>
              <img className="cursor-pointer h-[60px]" src={imgRoads["bus"]} alt=""></img>
            </div>
          </div>

        {
            isFetching&&isLoading?<div className="w-full flex justify-center mt-[100px]"><div><RingLoader
            color={"#F37022"}
            loading={isLoading}
            size={150}
            aria-label="Loading Spinner"
            data-testid="loader"
            />
            <p className="text-center">Загружаем...</p>
          </div>
          </div>:<div>{
            !isFetching
            ?routes.map(({info,duration,price,id},index)=>
                info.length>1
                ?<div className="flex gap-[40px]">
                  <div className="text-[16px]">
                    <p className="text-[14px]">Длительность</p>
                    <p>{secondsToHoursMinutes(duration)}</p>
                  </div>
                  <div className="text-[16px]">
                    <p className="text-[14px]">Цена</p>
                    <p>{Math.round(price)} руб</p>
                  </div>
                  <TransferRoute routes={info} />
                  </div>
                :
                info[0].route&&
                <div className="flex gap-[40px]">
                  <div className="text-[16px]">
                    <p className="text-[14px]">Длительность</p>
                    <p>{secondsToHoursMinutes(duration)}</p>
                  </div>
                  <div>
                    <p className="text-[14px]">Цена</p>
                    <p>{Math.round(price)} руб</p>
                  </div>
                  
                  <div className="border-2 p-[5px] mb-[40px]">
                  <DirectRoute route={info[0].route}/>
                  </div>
                  
                </div>

            )
          :<></>
          }</div>
            
        }
        </div>
    )
}


export default RouteList