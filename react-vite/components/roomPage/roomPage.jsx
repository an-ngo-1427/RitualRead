import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { io } from 'socket.io-client'

function RoomPage() {
    const [connected, setConnected] = useState(false);
    const [roomData, setRoomData] = useState(null);
    const { roomId } = useParams();

    useEffect(() => {
        const socket = io();

        socket.on('connect', () => {
            setConnected(true);
            socket.emit('join_room', { room_id: roomId });
        });

        socket.on('room_data', (data) => {
            setRoomData(data);
        });

        return () => {
            socket.disconnect();
        };
    }, [roomId]);

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
