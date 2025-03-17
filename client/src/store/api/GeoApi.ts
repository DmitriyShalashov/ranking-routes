import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { ITransfer } from '../../consts/types'

export interface IGeoPoint{
    lat:number
    lng:number
    name:string
    description:string
}



export const geoApi = createApi({
  reducerPath: 'geoApi',
  baseQuery: fetchBaseQuery({ baseUrl: 'http://127.0.0.1:5000/api/geo/' }),
  endpoints: (builder) => ({
    getCities: builder.query<string, string>({
      query: (name) => ({
        url:`geo_point/`,
        params:{
            "name":name
        }
    }),
    }),
  }),
})

export const { useGetCitiesQuery }=geoApi