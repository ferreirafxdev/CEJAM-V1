import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          900: "#0B254B",
          800: "#12356A",
          600: "#1D5FD1",
          50: "#EEF4FF",
        },
        accent: {
          500: "#2F9E63",
          200: "#D6E97A",
        },
      },
      boxShadow: {
        soft: "0 12px 32px -20px rgba(11, 37, 75, 0.45)",
      },
      keyframes: {
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(12px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "fade-in": {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
      },
      animation: {
        "fade-up": "fade-up 500ms ease-out both",
        "fade-in": "fade-in 350ms ease-out both",
      },
    },
  },
  plugins: [],
} satisfies Config;
