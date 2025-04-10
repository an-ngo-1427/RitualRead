import { useEffect, useState } from "react"
import { useNavigate, useParams,useBlocker} from "react-router-dom"
import GameCanvas from "../gamePage/gameCanvas"
import { io } from 'socket.io-client'

let socket
function RoomPage() {
    const [roomData, setRoomData] = useState(null);
    const { roomId } = useParams();
    const navigate = useNavigate();
    const [showExitDialog, setShowExitDialog] = useState(false);
    const [sio, setSio] = useState(null);
    const [gameStarted, setGameStarted] = useState(false);
    // useEffect to connect to the socket server

    // useEffect to connect socket
    useEffect(() => {
        socket = io()
        socket.on('connect', (message) => {
            console.log('conntecting to server...:', message);
            setSio(socket);
        });
        socket.on("connect_error", (err) => {
            console.log(`connect_error due to ${err.message}`);
        });
        socket.emit('joinRoom', roomId)
        socket.on('join_room', (data) => {
            setRoomData(data.room);
        });
        socket.on('leave_room', (data) => {
            setSio(null);
            setRoomData(data.room);

        });

        return () => {
            socket.disconnect();
        }
    },[])

    // Adding a warning when user navigate out of the room page
    useEffect(() => {
        history.pushState(null,"",window.location.href)
        const handlePopState = (event) => {
            event.preventDefault();
            setShowExitDialog(true);
        }

        window.addEventListener('popstate', handlePopState);
        return () => {
            window.removeEventListener('popstate', handlePopState);
        }
    },[])

    // Adding a warning when user refresh the page
    useEffect(() => {
        const handleNavigations = (event) => {
            const navigationEntry = performance.getEntriesByType('navigation')[0];
            console.log('navigationEntry:', navigationEntry);
            switch (navigationEntry.type) {
                case 'reload':
                    console.log('Page was reloaded');
                    event.preventDefault();
                    setShowExitDialog(true);
                    break;
                default:
                    break;
            }
        }
        window.addEventListener('beforeunload', handleNavigations);
        return () => {
            window.removeEventListener('beforeunload', handleNavigations);
        }
    }
    ,[])
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
        <div>
            {gameStarted? (<GameCanvas/>) :
               ( <div className="room-container">
                    <h1>Room Page</h1>
                    {roomData ? (
                        <div>
                            <h2>{roomData.name}</h2>
                            <div>
                                {roomData.members.map((member) => <div key={member.id}>{member.username}</div>)}
                            </div>
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
                    <button
                        className="start-game-btn"
                        onClick={() => {
                            setGameStarted(true);
                            socket.emit('start_game',{'players':roomData.members});
                        }}
                    >
                        Start Game
                    </button>
                    {showExitDialog && (
                        <div className="exit-dialog">
                            <p>Are you sure you want to exit the room?</p>
                            <button onClick={handleExitRoom}>Yes</button>
                            <button onClick={() => {
                                setShowExitDialog(false)
                                history.pushState(null, "", window.location.href);
                            }}
                            >No</button>
                        </div>
                    )}
                </div>)
            }
        </div>
    );
}

export default RoomPage;
