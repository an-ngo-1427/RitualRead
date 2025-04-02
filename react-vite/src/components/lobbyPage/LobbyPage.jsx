import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './LobbyPage.css';
import useSocket from '../../contexts/socketContext';

function LobbyPage() {
  const [rooms, setRooms] = useState([]);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [showJoinDialog, setShowJoinDialog] = useState(false);
  const [selectedRoomId, setSelectedRoomId] = useState(null);
  const [roomName, setRoomName] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [errors, setErrors] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchRooms();
  }, []);

  const fetchRooms = async () => {

    const response = await fetch('/api/rooms');
    const data = await response.json();
    setRooms(data.rooms);
  };

  const handleCreateRoom = async (e) => {
    e.preventDefault();
    const formData = new FormData()
    formData.append('name', roomName)
    const response = await fetch('/api/rooms', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    if (response.ok) {
      const newRoom = data.room
      setShowCreateDialog(false);
      console.log('New room:', newRoom);
      navigate(`/rooms/${newRoom.id}`)
    } else {
      setErrors(errorData.errors || ['An error occurred']);
    }
  };

  const handleJoinRoom = async (e) => {
    e.preventDefault();
    if (!selectedRoomId) return;

    try {
      const response = await fetch(`/api/rooms/${selectedRoomId}`, {
        method: 'POST',
      });
      const data = await response.json();
      if (response.ok) {
        setShowJoinDialog(false);
        // Navigate to room page
        navigate(`/rooms/${data.room.id}`);
      } else {
        console.error('Failed to join room');
      }
    } catch (error) {
      console.error('Error joining room:', error);
    }
  };

  const openJoinRoomDialog = (roomId) => {
    setSelectedRoomId(roomId);
    setShowJoinDialog(true);
  };

  const filteredRooms = searchTerm
    ? rooms.filter((roomDetails) =>
      roomDetails.name.toLowerCase().includes(searchTerm.toLowerCase()))
    : rooms;

  return (
    <div className="lobby-container">
      <h1>Lobby</h1>

      <div className="lobby-actions">
        <button
          className="create-room-btn"
          onClick={() => setShowCreateDialog(true)}
        >
          Create Room
        </button>

        <div className="search-container">
          <input
            placeholder="enter room name"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <button onClick={fetchRooms}>Search</button>
        </div>
      </div>

      <ul className="room-list">
        {filteredRooms.length > 0 ? (
          filteredRooms.map((roomDetails) => (
            <li
              key={roomDetails.id}
              className="room-item"
              onClick={() => openJoinRoomDialog(roomDetails.id)}
              id={roomDetails.id}
            >
              {roomDetails.name}
            </li>
          ))
        ) : (
          <li className="no-rooms">No rooms available</li>
        )}
      </ul>

      {/* Create Room Dialog */}
      {showCreateDialog && (
        <div className="dialog-backdrop">
          <div className="dialog">
            <h2>Create Room</h2>
            <form onSubmit={handleCreateRoom}>
              {errors.length && (
                <ul className="error-list">
                  {errors.map((err, index) => (
                    <li key={index} className="error-item">{err}</li>
                  ))}
                </ul>
              )}
              <div className="form-group">
                <label>Name</label>
                <input
                  placeholder="Enter room name"
                  value={roomName}
                  onChange={(e) => setRoomName(e.target.value)}
                  required
                />
              </div>
              <div className="dialog-actions">
                <button className="create-btn" type="submit">Create</button>
                <button
                  type="button"
                  className="close-btn"
                  onClick={() => {
                    setShowCreateDialog(false);
                    setErrors([]);
                  }}
                >
                  Close
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Join Room Dialog */}
      {showJoinDialog && (
        <div className="dialog-backdrop">
          <div className="dialog">
            <h2>Join Room</h2>
            <p>Do you want to join this room?</p>
            <div className="dialog-actions">
              <button onClick={handleJoinRoom}>Enter Room</button>
              <button
                className="close-btn"
                onClick={() => setShowJoinDialog(false)}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}



export default LobbyPage;
