import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import compression from "vite-plugin-compression";

export default defineConfig({
  plugins: [
    react(),
    compression({ algorithm: "brotliCompress" }), // Génère fichiers .br
  ],
  server: {
    port: 5173,
  },
  build: {
    sourcemap: false,
    minify: "terser", // Minification agressive
  },
});
