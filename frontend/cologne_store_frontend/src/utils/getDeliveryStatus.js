export function getDeliveryStatus(deliveryDateString) {

    const deliveryDate = new Date(deliveryDateString);
    const today = new Date();
    deliveryDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);
    const diffTime = deliveryDate - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays > 1) {
        return { text: `${diffDays} days left!`, status: "Order received" };
    } else if (diffDays === 1) {
        return { text: "1 day left", status: "On the way" };
    } else if (diffDays === 0) {
        return { text: "Today", status: "Arrived" };
    } else {
        return { text: "Delivered", status: "Completed" };
    }
}