import CologneGrid from "../components/products/cologneGrid.jsx"

export default function Home(){
    return (
        <main className="home-container">
        <section>
        <h2 className="cologne-grid-title">Current Collection</h2>
       <CologneGrid/>
        </section>
        </main>
    )
}