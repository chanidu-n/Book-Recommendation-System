import React, { useState } from 'react';


function Chatbot() {
const [message, setMessage] = useState('');
const [chat, setChat] = useState([]);


const sendMessage = async () => {
const response = await fetch('http://127.0.0.1:5000/chat', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ message })
});


const data = await response.json();


setChat([...chat, { user: message, bot: data.reply }]);
setMessage('');
};


return (
<div style={{ border: '1px solid #ccc', padding: '20px' }}>
<h3>🤖 Book Assistant</h3>


{chat.map((c, i) => (
<div key={i}>
<p><b>You:</b> {c.user}</p>
<p><b>Bot:</b> {c.bot}</p>
</div>
))}


<input
value={message}
onChange={e => setMessage(e.target.value)}
placeholder="Ask me about books"
/>
<button onClick={sendMessage}>Send</button>
</div>
);
}


export default Chatbot;