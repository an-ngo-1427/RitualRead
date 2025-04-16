import {useContext, useEffect, useRef} from "react"
import './gameCanvas.css'
import useUser from "../../contexts/userContext"
function GameCanvas(sio,game) {
    const {user,getUser,setUser} = useUser()
    const canvas1Ref = useRef(null)
    const canvas2Ref = useRef(null)
    useEffect(()=>{
        const context1 = canvas1Ref.current? canvas1Ref.current.getContext('2d') : null
        const context2 = canvas2Ref.current? canvas2Ref.current.getContext('2d') : null

    },[])
    return (
        <div>
            <h1>Game canvas</h1>
            {game.map((playerGame)=>{
                if(playerGame.player.username === user.username){
                    return (
                            <canvas ref={canvas1Ref} width={800} height={600}></canvas>
                    )}
                else{
                    return (
                            <canvas ref={canvas2Ref} width={800} height={600}></canvas>
                    )}
                })
            }

        </div>
    )
}

export default GameCanvas
