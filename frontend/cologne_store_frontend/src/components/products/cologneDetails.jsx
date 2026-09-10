/*Imagem grande a esquerda, com detalhes a direita e children dos botoes de compra
abaixo dos detalhes */
import priceCurrency from "../../utils/priceFormat.js"
import { PackageX } from "lucide-react"
export function CologneDetails({cologne, children}){
    
    return(
        <section className="cologne-details-box">
          <article className="cologne-details-card">
            <img className="cologne-details-img" src={cologne.image_url}/>
            <div className="cologne-details-titles">
              <p className="cologne-details-titles-name">{cologne.name}</p>
              <p className="cologne-details-titles-brand">{cologne.brand}</p>
            </div>
            <div className="cologne-details-info">
              <p className="cologne-details-info-price">{priceCurrency(cologne.price)}</p>
              <p className="cologne-details-info-amount">{cologne.amount}</p>
              {cologne.amount==0 && (
                <div className="cologne-unavailable">
                 <PackageX className="cologne-unavailable-icon"/>
                 <p className="cologne-unavailable-text">Sold out!</p>
                </div>
              )}
            </div>
          </article>
          <div className="cologne-details-buttons">
           {children}
          </div>
        </section>
    )
}