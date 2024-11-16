import { useEffect } from 'react';
import { useRouter } from 'next/router';
import '../styles/globals.css'; // Import global styles
import '../styles/login.css'; // Import login styles
import '../styles/create-account.css'; // Import create account styles
import '../styles/page.css'; // Import page styles

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