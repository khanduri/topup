// import type { Config } from "tailwindcss";
import colors from "tailwindcss/colors";

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      keyframes: {
        wiggle: {
          "0%, 100%": { transform: "rotate(-3deg)" },
          "50%": { transform: "rotate(3deg)" },
        },
      },
      animation: {
        wiggle: "wiggle 1s ease-in-out infinite",
      },
      colors: {
        // primary: colors.indigo,
        primary: {
          50: "#f3f6fb",
          100: "#e3eaf6",
          200: "#cddcf0",
          300: "#abc4e5",
          400: "#83a7d7",
          500: "#668acc",
          600: "#5271be",
          700: "#475fae",
          800: "#3f4f8e",
          900: "#364472",
          950: "#252b46",
        },
        complementary: colors.yellow,
        // secondary: colors.purple,
        secondary: {
          50: "#eafbff",
          100: "#cff5ff",
          200: "#aaefff",
          300: "#70e9ff",
          400: "#2dd7ff",
          500: "#00b6ff",
          600: "#008dff",
          700: "#0073ff",
          800: "#0061df",
          900: "#0057ae",
          950: "#02264b",
        },
        action: {
          50: "#feffe2",
          100: "#fbffc0",
          200: "#f3ff88",
          300: "#e7ff44",
          400: "#d6ff0d",
          500: "#b7f500",
          600: "#8cc500",
          700: "#699500",
          800: "#527000",
          900: "#466106",
          950: "#233700",
        },
      },
    },
  },
  plugins: [],
};
