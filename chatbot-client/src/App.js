import React, { useState } from 'react';
import axios from 'axios';

function Chatbot() {
    const [input, setInput] = useState('');
    const [responses, setResponses] = useState([]);

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/predict', {
                description: input
            });
            setResponses([...responses, { query: input, reply: response.data.solution }]);
            setInput('');
        } catch (error) {
            console.error('Error during API call', error);
        }
    };

    return (
        <div>
            <h1>IT Support Chatbot</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Describe your IT issue..."
                />
                <button type="submit">Send</button>
            </form>
            <div>
                {responses.map((exchange, index) => (
                    <p key={index}><strong>You:</strong> {exchange.query} <br /><strong>Bot:</strong> {exchange.reply}</p>
                ))}
            </div>
        </div>
    );
}

export default Chatbot;