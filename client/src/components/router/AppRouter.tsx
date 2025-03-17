import { Route, Routes } from "react-router-dom"
import publicRoutes from "../../consts/routes"

function AppRouter(){
    return (
        <Routes>
        {
            publicRoutes.map(({path,component})=>
                <Route path={path} element={component}></Route>
            )
        }
        </Routes>
    )
}


export default AppRouter