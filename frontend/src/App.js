import React, { useState } from 'react';
import Dashboard from './Dashboard';


function App() {
const [genre, setGenre] = useState('Fantasy');
const [pages, setPages] = useState(300);
const [difficulty, setDifficulty] = useState(2);
const [result, setResult] = useState(null);


const recommend = async () => {
const response = await fetch('http://127.0.0.1:5000/recommend', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ genre, pages, difficulty })
});


const data = await response.json();
setResult(data);
};


return (
<div style={{ padding: '40px' }}>
<h1>📚 Smart Book Advisor</h1>


<select onChange={e => setGenre(e.target.value)}>
<option>Fantasy</option>
<option>SelfHelp</option>
<option>Education</option>
</select>


<input type="number" value={pages} onChange={e => setPages(e.target.value)} />
<input type="number" value={difficulty} onChange={e => setDifficulty(e.target.value)} />


<button onClick={recommend}>Analyze</button>


<Dashboard result={result} />
</div>
);
}


export default App;