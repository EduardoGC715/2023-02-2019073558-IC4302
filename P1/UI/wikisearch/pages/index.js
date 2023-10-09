import Head from 'next/head';
import styles from '../styles/Home.module.css';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { getLogin } from '../lib/loginAPI';
import Link from 'next/link'
import Bus from '../utils/Bus'

// Código basado de:
// https://medium.com/@jaouad_45834/building-a-flash-message-component-with-react-js-6288da386d53

export const Flash = () => {
  let [visibility, setVisibility] = useState(false);
  let [message, setMessage] = useState('');
  let [type, setType] = useState('');

  useEffect(() => {
    Bus.addListener('flash', ({ message, type }) => {
      setVisibility(true);
      setMessage(message);
      setType(type);
      setTimeout(() => {
        setVisibility(false);
      }, 4000);
    });


  }, []);

  useEffect(() => {
    if (document.querySelector('.close') !== null) {
      document.
        querySelector('.close').
        addEventListener('click', () => setVisibility(false));
    }
  })

  return (
    visibility && <div className={`alert alert-${type}`}>
      <span className="close"><strong>X</strong></span>
      <p>{message}</p>
    </div>
  )
}

export default function Home() {
  if (typeof window !== 'undefined') {
    window.flash = (message, type = "success") => Bus.emit('flash', ({ message, type }));
  }

  const [email, setEmail] = useState(null)
  const [password, setPassword] = useState(null)
  const router = useRouter();

  async function handleOnSubmit(e) {
    e.preventDefault();
    console.log(email, password);
    const login = await getLogin(email, password);
    console.log(login);
    if (!login.hasOwnProperty("error")) {
      console.log("Logged in");
      localStorage.setItem('login', JSON.stringify({email, password}));
      router.push('/search');
    } else {
      window.flash('ERROR: The user does not exist', 'error')
      console.log('User does not exist');

    }
  }

  return (
    <div className={styles.container}>
      <Head>
        <title>WikiSearch</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <Flash />
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
        <Link href="/register"><button className={styles.buttonT1}>Sign Up</button></Link>
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
