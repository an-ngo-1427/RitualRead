import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    open: true,
    proxy: {
      "/api":{
        target:"http://127.0.0.1:5000",
      },
      "/socket.io":{
        target:"ws://127.0.0.1:5000",
      },
      // '/socket.io': {
      //   target: 'http://localhost:5000',
      //   ws: true
      // }
    },
  },
})
