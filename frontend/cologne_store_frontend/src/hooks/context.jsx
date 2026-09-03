import { createContext, useContext, useState } from "react"

const UserContext = createContext(null);
const VerifyMailContext = createContext(null);
const PasswordResetContext = createContext(null);

export function UserProvider({children}){
    const [user,setUser] = useState(null);
    
    return(
        <UserContext.Provider value={{user,setUser}}>
            {children}
        </UserContext.Provider>
    )
}

export function VerifyMailProvider({children}){
    const [isVerified,setIsVerified] = useState(null);

    return(
        <VerifyMailContext.Provider value={{isVerified,setIsVerified}}>
            {children}
        </VerifyMailContext.Provider>
    )
}

export function PasswordResetProvider({children}){
    const [reset,setIsReset] = useState(null);

    return(
        <PasswordResetContext value={{reset,setIsReset}}>
            {children}
        </PasswordResetContext>
    )
}

export function useUser(){
    return useContext(UserContext);
}

export function useVerifyMail(){
   return useContext(VerifyMailContext);
}

export function useReset(){
    return useContext(PasswordResetContext);
}