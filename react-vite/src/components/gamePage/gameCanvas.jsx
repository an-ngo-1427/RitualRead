import {useEffect, useRef} from "react"
import './gameCanvas.css'
function GameCanvas(monsters,sio,game) {
    console.log('in canvas page')
    const canvasRef = useRef(null)
    useEffect(()=>{
        const canvas = canvasRef.current
        const context = canvas.getContext('2d')
        context.fillText()
    },[])
    return (
        <div>
            <canvas className="game_canvas"  ref={canvasRef}>

            </canvas>
        </div>
    )
}

export default GameCanvas
