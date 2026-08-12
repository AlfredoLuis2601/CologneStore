export function HomeTitle(){
    //Posteriormente envolver o container com o link para o home
    return(
        <div className = "title-container">
          <img className ="cologne-icon"src={cologneImg}></img>
          <h1 className="home-page-title">Cologne Store</h1>
        </div>
    )
}