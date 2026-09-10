import { Outlet } from "react-router"
import { HomeTitle } from "./Title"
import { CircleCheck } from "lucide-react";
import ErrorUI from "../ui/errorState.jsx";
import { LoadState } from "../ui/loadingState.jsx";
import "./authLayout.css"
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

export function AuthStructureLayout({title,loading = false, error = null,success = false,footer = null,children, message = null}){

  return (
    <>
      <div className="auth-page-title-box">
        <h2 className="title">{title}</h2>
      </div>

      {children}

      {loading && <LoadState size="sm" message="Loading..." />}

      {error && (
        <ErrorUI
          size="sm"
          code={error.code}
          message={error.message}
          variant={error.variant}
        />
      )}

      {success && (
        <div className="successfull-auth-box">
          <CircleCheck className="svg-check-sm" />
          <p className="successfull-auth-text-sm">{message}</p>
        </div>
      )}

      {footer && <div className="support-links-box">{footer}</div>}
    </>
  );
}
