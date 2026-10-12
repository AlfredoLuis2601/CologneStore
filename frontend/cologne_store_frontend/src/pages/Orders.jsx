import { getOrders } from "../services/cologneService.js"
import { ErrorUI } from "../components/ui/errorState.jsx"
import { LoadState } from "../components/ui/loadingState.jsx"
import { useService } from "../hooks/useFetch.jsx"
import { getDeliveryStatus } from "../utils/getDeliveryStatus.js"
import { PackageX } from "lucide-react"
import { Header } from "../components/layout/Header.jsx"
import "../components/layout/Orders.css";

export function Orders() {
    const { data, loading, error } = useService(getOrders);

    if (loading) {
        return <LoadState message={"Loading..."} size={"lg"} />;
    }

    if (error) {
        return <ErrorUI message="Error loading orders." size="lg" />;
    }

    return (
        <>
        <Header />
        <main className="orders-container">
            <h2>My Orders</h2>

            {(!data || data.length === 0) ? (
                <div className="empty-orders">
                    <PackageX size={48} strokeWidth={1.5} />
                    <p>You haven't placed any orders yet.</p>
                </div>
            ) : (
                <section className="orders-section">
                    {data.map((orderGroup, index) => (
                        <article key={index} className="order-group-card">
                            <h3>Order #{index + 1}</h3>
                            
                            <ul className="items-list">
                                {orderGroup.map((item) => {
                                    const deliveryInfo = getDeliveryStatus(item.delivery_date);
                                    
                                    return (
                                        <li key={item.item_id} className="item-card">
                                            <div className="delivery-badge">
                                                <p><strong>{deliveryInfo.status}:</strong></p> {deliveryInfo.text}
                                            </div>

                                            <div className="item-content">
                                                <img src={item.img} alt={item.name || "Product"} className="product-image" />
                                                
                                                <div className="item-details">
                                                    <p className="product-name">{item.name}</p>
                                                    <p className="product-amount">Amount : {item.amount}</p>
                                                </div>
                                            </div>
                                        </li>
                                    );
                                })}
                            </ul>
                        </article>
                    ))}
                </section>
            )}
        </main>
        </>
    );
}