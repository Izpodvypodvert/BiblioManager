import LoginForm from "../components/LoginForm"
import { login } from "../utils/api"

const LoginPage = () => {
    const handleLogin = async (username, password) => {
        await login(username, password)
    }

    return (
        <div>
            <LoginForm onLogin={handleLogin} />
        </div>
    )
}

export default LoginPage
