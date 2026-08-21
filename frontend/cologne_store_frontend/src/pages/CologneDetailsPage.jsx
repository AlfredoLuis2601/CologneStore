import { useParams } from "react-router"

export function CologneDetailsPage(){
    //Chamar getCoalogneById para renderizar a pagina dentro do effect
    const params = useParams();
    console.log(params.uid);
    return(
        <>
        <h1>Details Page</h1>
        </>
    )
}