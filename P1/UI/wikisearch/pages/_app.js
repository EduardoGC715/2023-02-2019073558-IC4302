import '../styles/global.css'
import { StrictMode } from 'react'

// This default export is required in a new `pages/_app.js` file.
export default function MyApp({ Component, pageProps }) {
  return <StrictMode><Component {...pageProps} /></StrictMode>
}