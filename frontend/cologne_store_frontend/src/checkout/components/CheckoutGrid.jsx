import { CartItem } from "../components/cartItem.jsx"
import "../style/checkoutGrid.css";

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



