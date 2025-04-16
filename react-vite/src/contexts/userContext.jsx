import {createContext, useContext, useState} from 'react';
import { useNavigate } from 'react-router-dom';

const UserContext = createContext();

export function UserProvider({ children }) {
    const [user,setUser] = useState(null);

    const getUser = async () => {
        const response = await fetch('/api/auth/');
        const data = await response.json();
        if (response.ok) {
            setUser(data.user);
        } else {
            setUser(null);
        }
    }
const value = {
    user,
    getUser,
    setUser
}
return (
    <UserContext.Provider value={value}>
        {children}
    </UserContext.Provider>

)
}

function useUser() {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error('useUser must be used within a UserProvider');
    }
    return context;
}
export default useUser;
