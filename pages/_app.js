import { useEffect } from 'react';
import { useRouter } from 'next/router';
import '../styles/login.css';
import '../styles/create-account.css';

function MyApp({ Component, pageProps }) {
  const router = useRouter();

  useEffect(() => {
    if (router.pathname === '/') {
      router.push('/login');
    }
  }, [router]);

  return <Component {...pageProps} />;
}

export default MyApp;