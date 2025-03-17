import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { ITransfer } from '../../consts/types'


interface ITransferPrompt{
  frm:{
    lng:number
    lat:number
  }
  to:{
    lng:number
    lat:number
  }
  date:string
  transfers:boolean
}



export const transferApi = createApi({
  reducerPath: 'transferApi',
  baseQuery: fetchBaseQuery({ baseUrl: 'http://127.0.0.1:5000/api/route/' }),
  endpoints: (builder) => ({
    getTransfers: builder.mutation<string, ITransferPrompt>({
      query: (body) => ({
        method:"POST",
        url:`get_route/`,
        body
    }),
    }),
  }),
})

export const { useGetTransfersMutation }=transferApi