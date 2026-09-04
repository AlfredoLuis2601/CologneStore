import { createContext, useContext, useState } from "react"

const UserContext = createContext(null);
const VerifyMailContext = createContext(null);
const PasswordResetContext = createContext(null);

export function UserProvider({children}){
    const [user,setUser] = useState(null);
    const access_token = localStorage.getItem("access_token");
    const refresh_token = localStorage.getItem("refresh_token");
    if(!access_token && !refresh_token) return;
    try{

      const response = api.get("/current_user");
      console.log(response.user_information);
     setUser(response.user_information);
    }catch(e){
        setUser(null);
    }
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
    const [reset,setReset] = useState(null);

    return(
        <PasswordResetContext.Provider value={{reset,setReset}}>
            {children}
        </PasswordResetContext.Provider>
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