import { useDispatch, useSelector } from "react-redux"
import { RootState } from "../../store"
import { setIsSearchClicked, setSearchQuery } from "../../store/slices/SearchSlice"
import { useGetCitiesQuery } from "../../store/api/GeoApi"
import { useEffect, useRef, useState } from "react"
import { IGeoPoint } from "../../store/api/GeoApi"
import { setGeoQuery } from "../../store/slices/GeoSlice"

function Search() {
    
    const searchQuery=useSelector((state:RootState)=>state.search.searchQuery)
    const dispatch=useDispatch()
    const selectedCities=useSelector((state:RootState)=>state.geo)
    const {data:dataFrm,isSuccess:isSuccessFrm} = useGetCitiesQuery(searchQuery.frm,{skip:searchQuery.frm.length < 3})
    const {data:dataTo,isSuccess:isSuccessTo} = useGetCitiesQuery(searchQuery.to,{skip:searchQuery.to.length < 3})

    const [citesFrm, setCitiesFrm]=useState([] as IGeoPoint[])
    const [citesTo, setCitiesTo]=useState([] as IGeoPoint[])

    const [showFrmDropDown, setFrmShowDropdown]=useState(false)
    const [showToDropDown, setToShowDropdown]=useState(false)

    function handleFrmInputChange(e: React.ChangeEvent<HTMLInputElement>){
        const value = e.target.value;
        dispatch(setSearchQuery({...searchQuery, frm:value}))
      };
    function handlToInputChange(e: React.ChangeEvent<HTMLInputElement>){
        const value = e.target.value;
        dispatch(setSearchQuery({...searchQuery, to:value}))
      };

    useEffect(() => {
    if (isSuccessFrm && dataFrm) {
        setFrmShowDropdown(true);
        setCitiesFrm(JSON.parse(dataFrm).data)
    }
    }, [isSuccessFrm, dataFrm]);

    useEffect(() => {
        if (isSuccessTo && dataTo) {
            setToShowDropdown(true);
            setCitiesTo(JSON.parse(dataTo).data)
        }
        }, [isSuccessTo, dataTo]);

    
    const search=()=>{
        dispatch(setIsSearchClicked(true))
    }
    const dropdownFrm=useRef<HTMLUListElement>(null)
    const dropdownTo=useRef<HTMLUListElement>(null)

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
          if (dropdownFrm.current && !dropdownFrm.current.contains(event.target as Node)) {
            setFrmShowDropdown(false); 
          }
          if (dropdownTo.current && !dropdownTo.current.contains(event.target as Node)) {
            setToShowDropdown(false); 
          }
        };
    
        document.addEventListener("mousedown", handleClickOutside);
    
        return () => {
          document.removeEventListener("mousedown", handleClickOutside);
        };
      }, []);
    return (
        
        <div className="w-fit gap-[25px] bg-[#F37022] items-center rounded-[10px] flex p-[15px] shadow-xl hover:shadow-2xl">
                <div className="flex flex-col h-[80px] justify-between">
                    <div className="mb-[5px] h-[40px] text-[18px] text-white flex justify-between items-center"><p>Откуда</p> 
                        {selectedCities.frm?<div className="text-[12px] text-gray-200 flex gap-[10px] items-center">
                            <div>
                            <p><span className="text-[14px]">Выбран: </span>{selectedCities.frm.name}</p>
                            </div>
                        </div>
                        :<p></p>
                    }</div>
                    <input className="rounded-[7px] w-[300px] p-[5px] outline-none" value={searchQuery.frm} defaultValue={""} placeholder="Найти"
                        onChange={(e)=>{handleFrmInputChange(e)}}
                    ></input>
                   
                    <ul ref={dropdownFrm} className="top-[175px] absolute bg-white w-[300px]">
                        {
                            showFrmDropDown&&citesFrm&&citesFrm.map((city)=>
                            <li onClick={(e) => {
                                dispatch(setSearchQuery({...searchQuery, frm:city.name}))
                                dispatch(setGeoQuery({...selectedCities,frm:city}))
                            }} className="cursor-pointer p-[5px] border-2">{city.name}, {city.description}</li>
                        )
                        }
                    </ul>
                </div>

                <div className="flex flex-col h-[80px] justify-between">
                <div className="mb-[5px] h-[40px] text-[18px] text-white flex justify-between items-center"><p>Куда</p> 
                    {selectedCities.to&&<div className="text-[12px] text-gray-200 flex items-center gap-[10px]">
                        <div className="">
                        <p><span className="text-[14px]">Выбран: </span>{selectedCities.to.name}</p>
                        </div>
                            </div>
                        }</div>
                    <input className="rounded-[7px] w-[300px] p-[5px] outline-none" value={searchQuery.to} defaultValue={""} placeholder="Найти"
                        onChange={(e) => handlToInputChange(e)}
                    ></input>
                    
                    <ul ref={dropdownTo} className="top-[175px] absolute bg-white w-[300px]">
                        {
                            showToDropDown&&citesTo&&citesTo.map((city)=>
                            <li onClick={() => {
                                dispatch(setSearchQuery({...searchQuery, to:city.name}))
                                dispatch(setGeoQuery({...selectedCities,to:city}))
                            }
                            } className="cursor-pointer p-[5px] border-2">{city.name}, {city.description}</li>
                        )
                        }
                    </ul>
                </div>
                <div className="flex flex-col h-[80px] justify-between">
                    <p className="mb-[5px] mt-[4px] text-[18px] text-white ">Туда</p>
                    <input type="date" className="rounded-[7px] p-[5px] outline-none"
                        onChange={(e)=>dispatch(setSearchQuery({...searchQuery, date:e.target.value}))}
                    ></input>                
                    </div>
                <div className="flex flex-col h-[80px] justify-between">
                    <p className="mb-[5px] mt-[4px] text-[18px] text-white">Обратно</p>
                    <input type="date" className="rounded-[7px] p-[5px] outline-none"></input>
                </div>
                <button className="text-black linespace-none rounded-[10px] px-[10px] py-[5px] bg-white hover:bg-slate-100 shadow-xl hover:shadow-2xl"
                    onClick={()=>{search()}}
                >Найти</button>
            
        </div>
    )    
}

export default Search