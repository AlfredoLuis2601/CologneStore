import { useState, useRef, useEffect } from "react";
import { Link, useNavigate } from "react-router";
import { CircleUser, Package, ShoppingCart, LogOut } from "lucide-react";
import "../layout/Login.css";
import { useUser } from "../../hooks/context.jsx";
import { logout } from "../../services/authService.js";

export function Login() {
    const { user, setUser } = useUser();
    const [isOpen, setIsOpen] = useState(false);
    const menuRef = useRef(null);
    const navigate = useNavigate();

    const user_info = user || null;

    useEffect(() => {
        function handleClickOutside(event) {
            if (menuRef.current && !menuRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    const handleLogoutClick = async () => {
        setIsOpen(false);
        try {
            await logout();
        } catch (error) {
            console.error(error);
        } finally {
            if (setUser) setUser(null);
           
        }
    };

    return (
        <>
            {!user_info && (
                <Link to={"/auth"} style={{ textDecoration: "none", color: "white" }}>
                    <div className="login-header-container">
                        <CircleUser style={{ color: "blue" }} />
                        <p className="login-header-text">Login</p>
                    </div>
                </Link>
            )}

            {user && (
                <div className="user-menu-container" ref={menuRef}>
                    <button
                        onClick={() => setIsOpen(!isOpen)}
                        className="user-avatar-button"
                    >
                        <img 
                            src={`https://ui-avatars.com/api/?name=${user?.email}&background=random&color=0f0f0f`} 
                            alt="Avatar do usuário" 
                            className="user-avatar-image"
                        />
                    </button>

                    {isOpen && (
                        <div className="dropdown-menu">
                            <div className="dropdown-header">
                                <p className="dropdown-title">Account</p>
                                <p className="dropdown-email">{user?.email}</p>
                            </div>

                            <button
                                onClick={() => { setIsOpen(false); navigate('/orders'); }}
                                className="dropdown-item"
                            >
                                <Package size={16} /> Orders
                            </button>

                            <button
                                onClick={() => { setIsOpen(false); navigate('/checkout'); }}
                                className="dropdown-item"
                            >
                                <ShoppingCart size={16} /> Cart
                            </button>

                            <div className="dropdown-divider"></div>

                            <button
                                onClick={handleLogoutClick}
                                className="dropdown-item dropdown-item-danger"
                            >
                                <LogOut size={16} /> Logout
                            </button>
                        </div>
                    )}
                </div>
            )}
        </>
    );
}