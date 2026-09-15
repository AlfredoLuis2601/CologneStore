import { useCart } from "../hooks/context"

export function CheckoutPage(){
    const {cart} = useCart();
    console.log(cart);
    return(
        <>
        </>
    )
}