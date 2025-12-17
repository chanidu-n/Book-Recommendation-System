import React from 'react';
import Chatbot from './Chatbot';


function Dashboard({ result }) {
return (
<div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
<div>
<h2>📊 Prediction Result</h2>
{result && (
<>
<p>Predicted Rating: {result.predicted_rating}</p>
<h4>Recommended Books</h4>
<ul>
{result.recommended_books.map((b, i) => (
<li key={i}>{b}</li>
))}
</ul>
</>
)}
</div>


<Chatbot />
</div>
);
}


export default Dashboard;