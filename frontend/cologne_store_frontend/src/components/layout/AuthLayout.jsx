import { Outlet } from "react-router"
import { HomeTitle } from "./Title"
export function AuthLayout(){
    //Essa div vai ser a borda padrao para todas as auth pages
    return(
        <main className="auth-wrapper">
          <header className="auth-header">
            <HomeTitle/>
          </header>
          <section className="auth-card">
            <Outlet />
          </section>
      </main>
    )
}