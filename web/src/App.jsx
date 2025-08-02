import { useState, useEffect } from 'react';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('/api/data')  // URL Flask-сервера
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch((err) => console.error('Ошибка:', err));
  }, []);

  return (
    <div>
      <h1>Сообщение из Flask:</h1>
      <p>{message}</p>
    </div>
  );
}

export default App
