export function AuthForms({func,credentials,setCredentials}){

 function handleDefault(e){
    e.preventDefault();
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
          <button className="auth-button" 
            type="submit"onClick={func}>
          </button>
      </form>
    )
}