import { useEffect } from "react"
import RouteList from "../components/UI/Routes/RouteList"
import Search from "../components/search/Search"

function Main(){
    return (
        <div className="w-full p-[80px] flex justify-center">
            <div>
            <Search/>
            <RouteList></RouteList>
            </div>
       
        </div>
    )
}


export default Main