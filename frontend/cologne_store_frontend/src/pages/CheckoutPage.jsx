import { useCart, useUser} from "../hooks/context.jsx"
import { CheckoutGrid } from "../components/ui/CheckoutGrid.jsx";
import { Header } from "../components/layout/Header.jsx";
import { useCologneSearch } from "../hooks/useCologneSearch.jsx";
import { createOrder } from "../services/cologneService.js";
import { ShoppingCart, CircleCheck} from "lucide-react"; 
import {ErrorUI} from "../components/ui/errorState.jsx"
import { LoadState } from "../components/ui/loadingState.jsx";
import { useState } from "react";
import { useNavigate } from "react-router";
import "../components/layout/checkoutPage.css";

export function CheckoutPage() {
  const { cart, clearCart } = useCart(); 
  const { searchError } = useCologneSearch();
  const navigate = useNavigate();
  const {user} = useUser();
  const [loadingCheckout, setLoadingCheckout] = useState(false);
  const [checkoutError, setCheckoutError] = useState(null);
  
  const [successMessage, setSuccessMessage] = useState(false);

  const calculateTotals = () => {
    let itemsTotal = 0;
    let shippingTotal = 0;
    let days = 0;
    cart.forEach(item => {
      itemsTotal += item.price * item.amount;
      if (item.delivery === "express") {
        shippingTotal += 7.99 
        days = 3;
      } else {
        shippingTotal += 4.99 
        days = 7;
      }
    });

    const grandTotal = itemsTotal + shippingTotal;
    return { itemsTotal, shippingTotal, grandTotal, days};
  };

  const { itemsTotal, shippingTotal, grandTotal, days } = calculateTotals();

  const handleCheckout = async () => {

    const now = Date.now(); 
    const daysInMs = days * 24 * 60 * 60 * 1000; 
    const deliveryDateMs = now + daysInMs;
    const deliveryDate = new Date(deliveryDateMs).toISOString();

    if (cart.length === 0) return;

    try {
      setLoadingCheckout(true);
      setCheckoutError(null);

      const salePayload = {
        items: cart.map(item => ({
          uid: item.id,
          amount: item.amount,
          delivery_date: deliveryDate
        })),
        email: user.email
      };

      await createOrder(salePayload);
      setSuccessMessage(true);
      clearCart();

      setTimeout(() => {
        navigate("/orders");
      }, 2500);

    } catch (err) {
      setCheckoutError({
        code: err?.code || "CHECKOUT_ERROR",
        message: err.message || "Failed to process order. Please try again.",
        variant: err?.category || "error"
      });
      setLoadingCheckout(false); 
    }
  };

  if (loadingCheckout && !successMessage) {
    return <LoadState size="lg" message="Processing your order..." />;
  }

  return (
    <div className="checkout-page-container">
      <Header />

      <main className="checkout-content">
        <h2 className="checkout-content-title">Checkout</h2>
        {successMessage && (
          <div className="success-banner">
            <CircleCheck className="success-icon" size={32} />
            <p>Purchase Succeeded! Redirecting to orders...</p>
          </div>
        )}

        {cart.length === 0 && !successMessage ? (
          <div className="empty-cart-container">
            <ShoppingCart size={64} className="empty-cart-icon" />
            <p>Your cart is empty.</p>
          </div>
        ) : !successMessage && (
          <div className="checkout-layout">
            <CheckoutGrid cart={cart} />

            <div className="checkout-summary-box">
              <p className="checkout-summary-info">Order Summary</p>
              <div className="summary-row">
                <span className="checkout-summary-info">Items Subtotal:</span>
                <span className="checkout-summary-info">${itemsTotal.toFixed(2)}</span>
              </div>
              <div className="summary-row">
                <span className="checkout-summary-info">Estimated Shipping:</span>
                <span className="checkout-summary-info">${shippingTotal.toFixed(2)}</span>
              </div>
              <div className="summary-row total">
                <span className="checkout-summary-info">Total: ${grandTotal.toFixed(2)}</span>
              </div>

              <button 
                className="finalize-payment-button" 
                onClick={handleCheckout}
                disabled={loadingCheckout}
              >
                Place your order
              </button>
            </div>
          </div>
        )}

        {searchError && (
          <ErrorUI 
            code={searchError.code} 
            message={searchError.message} 
            variant={searchError.variant}
            size="sm"
          />
        )}

        {checkoutError && (
          <ErrorUI 
            code={checkoutError.code} 
            message={checkoutError.message} 
            variant={checkoutError.variant}
            size="sm"
          />
        )}
      </main>
    </div>
  );
}