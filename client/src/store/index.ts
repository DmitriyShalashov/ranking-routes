import { configureStore } from '@reduxjs/toolkit'
import { combineReducers } from '@reduxjs/toolkit'
import { transferApi } from './api/TransferApi'
import searchReducer from './slices/SearchSlice';
import geoReducer from './slices/GeoSlice'
import { geoApi } from './api/GeoApi';
export const store = configureStore({
    reducer: combineReducers({
        [transferApi.reducerPath]:transferApi.reducer,
        [geoApi.reducerPath]:geoApi.reducer,
        search:searchReducer,
        geo:geoReducer
    }),
    middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(transferApi.middleware, geoApi.middleware)
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch