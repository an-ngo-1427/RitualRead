import { useContext, useEffect, useRef } from "react"
import './gameCanvas.css'
import useUser from "../../contexts/userContext"
function GameCanvas({ game }) {
    console.log('game:', game)
    const { user, getUser, setUser } = useUser()
    const canvasRefs = useRef([])
    // const [canvas1Ref,setCanvas1Ref] = useState(null)
    // const [canvas2Ref,setCanvas2Ref] = useState(null)
    console.log('canvas1Ref:', canvasRefs)
    useEffect(() => {
        canvasRefs.current.forEach((canvas, index) => {
            const ctx = canvas.getContext('2d')
            const playerGame = game.player_games[index]
            const player = playerGame.player
            const gameData = playerGame.game_data
            console.log('gameData:', gameData)
            // Draw the game data on the canvas
            ctx.fillStyle = 'red'
            ctx.fillRect(0, 0, 10,10)


        })
    }, [])
    return (
        <div>
            <h1>Game canvas</h1>
            {game.player_games.map((playerGame, index) => {
                return (
                    <canvas
                        key={playerGame.player.username}
                        // Assign each canvas element to an index in canvasRefs.current using a callback
                        ref={(el) => (canvasRefs.current[index] = el)}
                        width={800}
                        height={600}
                        data-player={playerGame.player.username}
                    ></canvas>
                )
            })}


        </div>
    )
}

export default GameCanvas
