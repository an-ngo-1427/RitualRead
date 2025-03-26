import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { io } from 'socket.io-client'
let socket
function RoomPage() {
    const [connected, setConnected] = useState(false);
    const [roomData, setRoomData] = useState(null);
    const { roomId } = useParams();

    useEffect(() => {
        console.log('socket:');
        socket = io();
        socket.on('connect', () => {
            console.log('conntecting to server...');
            setConnected(true);
            socket.emit('join_room', { room_id: roomId });
        });
        socket.on("connect_error", (err) => {
            console.log(`connect_error due to ${err.message}`);
          });
        socket.on('message', (data) => {
            console.log('message:', data);
        });

        return () => {
            socket.disconnect();
        };
    }, []);

    return (
        <div className="room-container">
            <h1>Room Page</h1>
            {!connected && <p>Connecting to server...</p>}

            {roomData ? (
                <div>
                    <h2>{roomData.name}</h2>
                    {/* Additional room content will go here */}
                </div>
            ) : (
                <p>Loading room data...</p>
            )}
        </div>
    );
}

export default RoomPage;
