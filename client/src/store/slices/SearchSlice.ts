import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface SearchPrompt{
    frm:string,
    to:string,
    date:string
}

interface SearchState {
  searchQuery: SearchPrompt;
  isSearchClicked: boolean;
}

const initialState: SearchState = {
  searchQuery: {
    frm:"",
    to:"",
    date:""
  },
  isSearchClicked: false,
};

const searchSlice = createSlice({
  name: 'search',
  initialState,
  reducers: {
    setSearchQuery: (state, action: PayloadAction<SearchPrompt>) => {
      state.searchQuery = action.payload;
    },
    setIsSearchClicked: (state, action: PayloadAction<boolean>) => {
      state.isSearchClicked = action.payload;
    },
  },
});

export const { setSearchQuery,setIsSearchClicked } = searchSlice.actions;
export default searchSlice.reducer;