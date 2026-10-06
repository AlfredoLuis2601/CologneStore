import { Trash } from "lucide-react";
import priceCurrency from "../../utils/priceFormat.js";
import { useCart } from "../../hooks/context.jsx";
import "../layout/cartItem.css";

export function CartItem({item}){
   const {updateItemDelivery,removeItem} = useCart();
   return(
     <li className="cart-item-box">
       <div className="cart-item-info">
          <img className= "cart-item-img" src={item.img}/>
          <div className="cart-item-details">            
            <span className="cart-item-name">{item.name}</span>
             <div className="cart-item-extra-info">
            <span className="cart-item-quantity">Quantity: {item.amount}</span>
            <span className="cart-item-price">{priceCurrency(item.price)}</span>
            </div>
          </div>
       </div>
       <section className="cart-item-actions">
        <div className="cart-item-delivery-options">
         <label className="delivery-card">
           <input type="radio" name={`delivery_type_${item.id}`} value={"standard"} onChange={(e)=> updateItemDelivery(item.id,e.target.value)}/>
           <div className="delivery-option">
            <p className="delivery-option-text">Standard Delivery</p>
            <span className="delivery-option-text">5 to 7 days - $4.99</span>
           </div>
         </label>

         <label className="delivery-card">
           <input type="radio" name={`delivery_type_${item.id}`} value={"express"}  onChange={(e)=> updateItemDelivery(item.id,e.target.value)}/>
           <div className="delivery-option">
            <p className="delivery-option-text">Express Delivery</p>
            <span className="delivery-option-text">2 to 3 days - $7.99</span>
           </div>
         </label>
        </div>
        <Trash className="remove-item-icon" onClick={()=> removeItem(item.id)}/>
       </section>
     </li>
   )
}