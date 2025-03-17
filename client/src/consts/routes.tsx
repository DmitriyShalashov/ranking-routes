import { JSX } from "react"
import Main from "../pages/Main"

interface IRoute{
    path:string,
    component:JSX.Element
}

const publicRoutes:IRoute[]=[
    {
        path:"/",
        component:<Main/>
    }
]

export default publicRoutes