import { getOrders } from "../services/cologneService.js"
import { ErrorUI } from "../components/ui/errorState.jsx"
import { LoadState } from "../components/ui/loadingState.jsx"
import { useService } from "../hooks/useFetch.jsx"
import { getDeliveryStatus } from "../utils/getDeliveryStatus.js"
import { PackageX } from "lucide-react"

export function Orders() {
    const { data, loading, error } = useService(getOrders);

    if (loading) {
        return <LoadState message={"Loading..."} size={"lg"} />;
    }
    if (error) {
        return <ErrorUI message="Error loading orders." size="lg" />;
    }
    return (
        <div className="orders-container">
            <h2 className="orders-title">My Orders</h2>

            {(!data || data.length === 0) ? (
                <div className="empty-orders">
                    <PackageX size={48} strokeWidth={1.5} />
                    <p>You haven't placed any orders yet.</p>
                </div>
            ) : (
                <div className="orders-list">
                    {data.map((orderGroup, index) => (
                        <div key={index} className="order-card">
                            <h3>Order #{index + 1}</h3>
                            
                            {orderGroup.map((item) => {
                                const deliveryInfo = getDeliveryStatus(item.delivery_date);
                                
                                return (
                                    <div key={item.item_id} className="item-row">
                                        <span>Amount: {item.amount}</span>
                                        <div className="delivery-badge">
                                            <strong>{deliveryInfo.status}:</strong> {deliveryInfo.text}
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
