import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import {IGeoPoint} from '../api/GeoApi'
interface GeoPrompt{
    frm:IGeoPoint,
    to:IGeoPoint,
}

const initialState: GeoPrompt = {
  frm:{} as IGeoPoint,
  to:{} as IGeoPoint
};

const geoSlice = createSlice({
  name: 'geo',
  initialState,
  reducers: {
    setGeoQuery: (state, action: PayloadAction<GeoPrompt>) => {
        state.frm=action.payload.frm
        state.to=action.payload.to
    },
  },
});

export const { setGeoQuery } = geoSlice.actions;
export default geoSlice.reducer;