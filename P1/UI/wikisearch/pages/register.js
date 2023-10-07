import Head from 'next/head';
import styles from '../styles/Home.module.css';
import { useEffect, useState } from 'react';
import { getRegister } from '../lib/registerAPI';
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

export default function Register() {
  if (typeof window !== 'undefined') {
    window.flash = (message, type = "success") => Bus.emit('flash', ({ message, type }));
  }
  const [email, setEmail] = useState(null)
  const [password, setPassword] = useState(null)
  const [phone, setPhone] = useState(null)
  const [name, setName] = useState(null)
  const [last_name1, setLastName1] = useState(null)
  const [last_name2, setLastName2] = useState(null)
  async function handleOnSubmit(e) {
    e.preventDefault();
    console.log(email, password, phone, name, last_name1, last_name2);
    if (password.length < 6) {
      console.log("Invalid Password");
      window.flash('ERROR: The password is shorter than 6 characters', 'error')
      return
    }
    const registro = await getRegister(email, password, phone, name, last_name1, last_name2);
    console.log(registro);
    if (!registro.hasOwnProperty("error")) {
      console.log("User created");
      window.flash('The user has been created', 'success')
      window.flash
    } else {
      console.log('User was not created');
      window.flash('ERROR: The user is already registered', 'error')
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

            <input className={styles.inputT1} type="password" placeholder="Password (At least 6 characters)" required
              onChange={e => setPassword(e.target.value)}
            />

            <input className={styles.inputT1} type="phone" placeholder="Phone: (Area Code) Number" required
              onChange={e => setPhone(e.target.value)}
            />
            <input className={styles.inputT1} type="name" placeholder="Name" required
              onChange={e => setName(e.target.value)}
            />
            <input className={styles.inputT1} type="last_name1" placeholder="Last Name 1" required
              onChange={e => setLastName1(e.target.value)}
            />
            <input className={styles.inputT1} type="last_name2" placeholder="Last Name 2" required
              onChange={e => setLastName2(e.target.value)}
            />
            <button className={styles.buttonT1} type="submit">Register</button>
          </form>
        </div>
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
