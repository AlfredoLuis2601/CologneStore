import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {BrowserRouter} from "react-router"
import {CartContextProvider, PasswordResetProvider, UserProvider, VerifyMailProvider} from "./hooks/context.jsx"
import './index.css'
import App from './App.jsx'


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <UserProvider> 
      <VerifyMailProvider>  
        <PasswordResetProvider>
          <CartContextProvider>
              <App/>
          </CartContextProvider>
         </PasswordResetProvider>  
      </VerifyMailProvider>  
      </UserProvider>
    </BrowserRouter>
  </StrictMode>,
)
