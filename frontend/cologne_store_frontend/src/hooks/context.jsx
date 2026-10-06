import { createContext, useContext, useEffect, useState } from "react"
import api from "../services/api.js";
const UserContext = createContext(null);
const VerifyMailContext = createContext(null);
const PasswordResetContext = createContext(null);
const CartContext = createContext(null);

export function UserProvider({children}){

    const [user,setUser] = useState(null);
    const access_token = localStorage.getItem("access_token");
    const refresh_token = localStorage.getItem("refresh_token");

    useEffect(()=>{
     async function restoreUser(){
        if(!access_token && !refresh_token) return;
        try{
          const response = await api.get("/users/current_user");
          setUser({
              email:response.user_information.username,
              id:response.user_information.user_id,
              role:response.user_information.role
            });
          
        }catch(e){
          setUser(null);
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
       }
     }
     restoreUser();
    },[])
    
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

export function CartContextProvider({children}){
    const [cart, setCart] = useState(()=>{
        const cart = localStorage.getItem("cart");
        return cart? JSON.parse(cart): [];
    });
    useEffect(()=>{
      localStorage.setItem("cart",JSON.stringify(cart));
    }, [cart])
   const updateItemDelivery = (id, newDeliveryType) =>{
     setCart(prevCart => prevCart.map(item =>
        item.id === id? {...item, delivery: newDeliveryType} : item
     )
    );
   }
   const removeItem = (id) => {
    setCart(prevCart => prevCart.filter(item => item.id != id));
   }
   const clearCart = () => {
  localStorage.removeItem("cart"); 
  setCart([]); 
};
    return(
        <CartContext.Provider value={{cart, setCart,updateItemDelivery,clearCart,removeItem}}>
            {children}
        </CartContext.Provider>
    )
}
export function useCart(){
    return useContext(CartContext);
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