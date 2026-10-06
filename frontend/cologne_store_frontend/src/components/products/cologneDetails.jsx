import priceCurrency from "../../utils/priceFormat.js"
import { PackageX } from "lucide-react"
import './cologneDetails.css'

export function CologneDetails({ cologne, children }) {
    return(
        <section className="cologne-details-container">
          <div className="cologne-details-grid">
            <div className="cologne-image-wrapper">
              <img className="cologne-details-img" src={cologne.image_url} alt={cologne.name} />
            </div>
            <div className="cologne-details-content">
              <div className="cologne-details-titles">
                <h1 className="cologne-details-titles-name">{cologne.name}</h1>
                <p className="cologne-details-titles-brand">{cologne.brand}</p>
              </div>

              <div className="cologne-details-info">
                <p className="cologne-details-info-price">{priceCurrency(cologne.price)}</p>
                <p className="cologne-details-info-amount">Available stock : {cologne.amount}</p>
                
                {cologne.amount === 0 && (
                  <div className="cologne-unavailable">
                    <PackageX className="cologne-unavailable-icon"/>
                    <p className="cologne-unavailable-text">Sold out!</p>
                  </div>
                )}
              </div>
              <div className="cologne-details-buttons">
                {children}
              </div>
            </div>
          </div>
        </section>
    )
}