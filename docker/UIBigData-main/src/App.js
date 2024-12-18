import { useEffect, useState } from 'react';
import './App.css';
import Container from './component/Container';
import Header from './component/Header';

function App() {
  const [page, setPage] = useState("pageTagXml.xml")

  return (
    <div style={{
      padding: '10px 60px',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      fontFamily: 'sans-serif',
      fontWeight: '100',
      color: '#333333',
      letterSpacing: '0.3px',
      wordSpacing: '1.5px'  
    }}>
      <Header page={page} setPage={setPage} />
      <Container page={page} setPage={setPage} />
    </div>
  );
}

export default App;
