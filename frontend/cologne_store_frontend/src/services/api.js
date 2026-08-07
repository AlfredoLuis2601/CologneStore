import axios from "axios"

//Começando a entender axios (conexão API com meu site)

const api = axios.create({
    baseURL:import.meta.env.VITE_BASE_URL,
    headers:{"X-Custom-Header":"foobar"},
    timeout:10000
});
export default api
//Adicionar erros retornados por falta de jwt, rolePermission