import { createContext, useContext } from "react";

const DatabaseContext = createContext();
export const DatabaseProvider = DatabaseContext.Provider;

export const useDatabase = () =>
    useContext(DatabaseContext);

export default DatabaseContext;

