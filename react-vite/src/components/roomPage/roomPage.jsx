import { useEffect, useState } from "react"
import { useNavigate, useParams,useBlocker} from "react-router-dom"

import { io } from 'socket.io-client'
let socket
function RoomPage() {
    const [connected, setConnected] = useState(false);
    const [roomData, setRoomData] = useState(null);
    const { roomId } = useParams();
    const navigate = useNavigate();
    const [showExitDialog, setShowExitDialog] = useState(false);
    // useEffect to connect to the socket server
    useBlocker((currentLocation, nextLocation) => {
        return currentLocation.pathname !== nextLocation.pathname
    })
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
    }, [roomId]);

    // useEffect to fetch room data
    useEffect(() => {
        const fetchRoomData = async () => {
            try {
                const response = await fetch(`/api/rooms/${roomId}`);
                const data = await response.json();
                if (!response.ok) {
                    // throw new Error('Failed to fetch room data');
                    console.error('Failed to fetch room data:', data);
                    navigate('/lobby');
                    return;
                }
                setRoomData(data.room);
            } catch (error) {
                console.error('Error fetching room data:', error);
            }
        };

        fetchRoomData();
    }, []);

    const handleExitRoom = async () => {
        const response = await fetch(`/api/rooms/${roomId}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            navigate('/lobby');
        } else {
            console.error('Failed to exit room');
        }

    }
    return (
        <div className="room-container">
            {/* <Prompt
                message={(location,action) => {
                    if (action == 'POP') {
                        return "Are you sure you want to exit room?";
                    }
                }}
            >

            </Prompt> */}
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
            <button
                className="exit-room-btn"
                onClick={() => setShowExitDialog(true)}
            >
                Exit room
            </button>
            {showExitDialog && (
                <div className="exit-dialog">
                    <p>Are you sure you want to exit the room?</p>
                    <button onClick={handleExitRoom}>Yes</button>
                    <button onClick={() => setShowExitDialog(false)}>No</button>
                </div>
            )}
        </div>
    );
}

export default RoomPage;
