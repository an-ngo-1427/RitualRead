import { defineConfig } from "vite";


// https://vitejs.dev/config/
export default defineConfig((mode) => ({
  server: {
    open: true,
    proxy: {
      "/api": "http://127.0.0.1:5000",
    },
  },
}));
