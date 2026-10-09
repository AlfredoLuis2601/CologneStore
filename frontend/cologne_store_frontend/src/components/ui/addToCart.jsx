import { useState } from "react";
import { useCart } from "../../hooks/context.jsx";
import { LoadState } from "./loadingState.jsx";
import ErrorUI from "./errorState.jsx";
import { CircleCheck } from "lucide-react";
import { Link } from "react-router"
import "./addToCart.css";

export function CartSection({cologne}){
   
   const [error, setError] = useState(null);
   const [loading, setLoading] = useState(false);
   const {setCart} = useCart();
   const [quantity, setQuantity] = useState(1);
   const [success, setSuccess] = useState(false);
   function handleCart(){
     try{
     setLoading(true);
     setError(null);
     if(quantity<=0){
       const e = new Error("Quantity must be greater than 0")
       e.code = 400;
       throw e;
     }
     setCart((prevCart)=>{
       const existingItem = prevCart.findIndex(item => item.id===cologne.uid);
       if (existingItem>=0){
          const updatedCart = [...prevCart]
          updatedCart[existingItem].amount+=quantity;
          return updatedCart;
       }
       return [...prevCart,{
         id: cologne.uid,
         amount: quantity,
         price: cologne.price,
         name: cologne.name,
         img: cologne.image_url,
         delivery: "standard"
       }]
     })
     setSuccess(true);
     setTimeout(()=>{
        setSuccess(false);
     },2000)
    }catch(e){
      setError({
        code:e?.code,
        message:e.message,
        variant:e?.category
      })
    }finally{
      setLoading(false);
    }

   }
   function handleDecrement(){
     setQuantity(count=> count-1);
   }

   function handleIncrement(){
     setQuantity(count=> count+1)
   }
   
   return(
    <>
     <div className="quantity-selector">

       <button className="decrement-button" onClick={handleDecrement} disabled={quantity<=1}>
           -
       </button>
       <span className="quantity">{quantity}</span>
       <button className="increment-button" onClick={handleIncrement} disabled={quantity>=cologne.amount}>
          +
       </button>

     </div>
     <div className="cart-buttons-container">
       {success && (
         <div className="successfull-auth-box">
          <CircleCheck className="svg-check-sm" />
          <p className="successfull-auth-text-sm">Product added to cart</p>
         </div>
       )}
       <button className="cart-button" onClick={handleCart}>
         Add to cart
       </button>
       <Link to={"/checkout"} style={{textDecoration:"none"}}>
         <button className="cart-button">
           Go to cart
         </button>
       </Link>
     </div>
     
     {loading && ( 
        <LoadState size="sm" message="Loading..."/>
      )}

     {error && (
        <ErrorUI
         size="sm"
         code={error.code}
         message={error.message}
        />
       )}
  </>
   )
}