import {useEffect, useRef} from "react"
function GameCanvas(monsters) {
    const canvasRef = useRef(null)
    useEffect(()=>{
        const canvas = canvasRef.current
        const context = canvas.getContext('2d')
        context.fillText()
    })
    return (
        <div>
            <canvas classname="game_canvas"  ref='canvasRef' width= '400px' height='300px'>
            </canvas>
        </div>
    )
}
