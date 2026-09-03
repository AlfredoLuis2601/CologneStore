export function AuthForms({func,credentials,setCredentials}){

 function handleDefault(e){
    e.preventDefault();
    func();
  }
 function handleChange(e){
    const {name,value} = e.target;
    setCredentials((prev)=>({
        ...prev,[name]:value
    }))
 }
    return(
      <form className="auth-forms-container" onSubmit={handleDefault}>
          <label htmlFor="email">
            <input id="email" name="email" 
              className="auth-input" type="text" 
              placeholder="email" value={credentials.email} 
              onChange={handleChange}
            />
          </label>
          <label htmlFor="password">
             <input id="password" name="password" 
              className="auth-input" type="text" 
              placeholder="password:" value={credentials.password} 
              onChange={handleChange}
             />
          </label>
          <button className="auth-button" type="submit">
            Enter
          </button>
      </form>
    )
}

export function AuthMailForms({handleClick, email, setEmail}){
  
  function handleDefault(e){
    e.preventDefault();
    handleClick();
  }

  function handleChange(e){
    setEmail(e.target.value);
  }

  return (
    <form className="auth-forms-container" onSubmit={handleDefault}>
      <label htmlFor="email">
         <input
         className="auth-input"
         type="text"
         id="email"
         name="email"
         placeholder="Enter your email:"
         value={email}
         />
      </label>
      <button className="auth-button" type="submit">
         Send request email
      </button>
    </form>
  )
}

export function AuthPasswordForms({handleClick, payload, setPayload}){
  function handleSubmit(e){
    e.preventDefault();
    handleClick();
  }

  function handleChange(e){
    const {name, value} = e.target;
    setPayload((prev)=> ({
     ...prev,[name]:value
    }))
  }

  return(
      <form className="auth-forms-container" onSubmit={handleSubmit}>
      <label htmlFor="new_password">
         <input
         className="auth-input"
         type="text"
         id="new_password"
         name="new_password"
         placeholder="Enter your new password:"
         value={payload.new_password}
         />
      </label>
       <label htmlFor="confirm_new_password">
         <input
         className="auth-input"
         type="text"
         id="confirm_new_password"
         name="confirm_new_password"
         placeholder="Confirm your new password:"
         value={payload.confirm_new_password}
         />
      </label>
      <button className="auth-button" type="submit">
         Send request email
      </button>
    </form>
  )
}