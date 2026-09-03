import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {BrowserRouter} from "react-router"
import {PasswordResetProvider, UserProvider, VerifyMailProvider} from "./hooks/context.jsx"
import './index.css'
import App from './App.jsx'


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <UserProvider> 
      <VerifyMailProvider>  
        <PasswordResetProvider>
              <App/>
         </PasswordResetProvider>  
      </VerifyMailProvider>  
      </UserProvider>
    </BrowserRouter>
  </StrictMode>,
)
