import { createContext, useContext ,useState} from "react";

const SocketContext = createContext()

export function SocketProvider({ children }){
    const [socket,setSocket] = useState(null);
    const [connected,setConnected] = useState(false);

    const socketConnect = () => {
        const socket = io();
        socket.on('connect', () => {
            console.log('conntecting to server...');
            setConnected(true);
        });
        socket.on("connect_error", (err) => {
            console.log(`connect_error due to ${err.message}`);
        });
        setSocket(socket);
        setConnected(true);
        return
    }

    const socketDisconnect = () => {
        if (socket) {
            socket.disconnect();
            setConnected(false);
            setSocket(null);
        }
    }

    const value = {
        socket,
        connected,
        socketConnect,
        socketDisconnect
    }

    return (
        <SocketContext.Provider value={value}>
            {children}
        </SocketContext.Provider>
    )
}

function useSocket() {
    const context = useContext(SocketContext);
    if (!context) {
        throw new Error("useSocket must be used within a SocketProvider");
    }
    return context;
}

export default useSocket
