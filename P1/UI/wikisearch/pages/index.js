import Head from 'next/head';
import styles from '../styles/Home.module.css';
import { useState } from 'react';
import { getLogin } from '../lib/loginAPI';
import Link from 'next/link'

export default function Home() {
  const [email, setEmail] = useState(null)
  const [password, setPassword] = useState(null)

  async function handleOnSubmit(e) {
    e.preventDefault();
    console.log(email, password);
    const login = await getLogin(email, password);
    console.log(login);
    if (!login.hasOwnProperty("error")) {
      console.log("Logged in");
    } else {
      console.log('User does not exist');
    }
  }

  function handleSignUp(e) {
    // Moverse a pagina de Sign Up


    console.log('hola');
  }

  return (
    <div className={styles.container}>
      <Head>
        <title>WikiSearch</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <h1 className={styles.title}>
          Login
        </h1>

        <p className={styles.description}>
          Get started with <span style={{ fontWeight: 700, color: "purple" }}>WikiSearch</span> today!
        </p>

        <div className={styles.formulario}>
          <form method="post" onSubmit={handleOnSubmit}>
            <input className={styles.inputT1} type="text" placeholder="Email" required
              onChange={e => setEmail(e.target.value)}
            />

            <input className={styles.inputT1} type="password" placeholder="Password" required
              onChange={e => setPassword(e.target.value)}
            />
            <button className={styles.buttonT1} type="submit">Login</button>
          </form>
        </div>
        < Link href="/register"><button className={styles.buttonT1}>Sign Up</button></Link>
      </main>

      <footer>
        <a
          href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by{' '}
          <img src="/vercel.svg" alt="Vercel" className={styles.logo} />
        </a>
      </footer>
    </div>

  );
}
