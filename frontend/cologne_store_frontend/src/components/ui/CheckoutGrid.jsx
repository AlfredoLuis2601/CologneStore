import { CartItem } from "../products/cartItem.jsx"
import "../layout/checkoutGrid.css";

export function CheckoutGrid({cart}){

    return(
        <ul className="cart-items-container">
            {cart.map(item => <CartItem 
            item={item}
            key={item.id}
            />)}
        </ul>
    )
}



