import { createContext, useContext } from "react";

const SocketContext = createContext()

export function SocketProvider(){
    const [socket,setSocket] = useState(null);
    const [connected,setConnected] = useState(false);

    const socketConnect = () => {
        const socket = io();
        socket.on('connect', () => {
            console.log('conntecting to server...');
            setConnected(true);
            socket.emit('join_room', { room_id: roomId });
        });
        socket.on("connect_error", (err) => {
            console.log(`connect_error due to ${err.message}`);
        });
        setSocket(socket);
    }

    const socketDisconnect = () => {
        if (socket) {
            socket.disconnect();
            setConnected(false);
        }
    }

    value = {
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

export function useSocket() {
    const context = useContext(SocketContext);
    if (!context) {
        throw new Error("useSocket must be used within a SocketProvider");
    }
    return context;
}
