import { useParams } from "react-router"

export function CologneDetailsPage(){
    const params = useParams();
    console.log(params.uid);
    return(
        <>
        <h1>Details Page</h1>
        </>
    )
}