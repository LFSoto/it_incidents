import React, { useState } from 'react';
import { TypeAnimation } from 'react-type-animation';
import axios from 'axios';

function Chatbot() {
    const [input, setInput] = useState('');
    const [responses, setResponses] = useState([]);

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:5000/predict', {
                description: input
            });
            setResponses([...responses, { query: input, reply: response.data.solution }]);
            setInput('');
        } catch (error) {
            console.error('Error during API call', error);
        }
    };

    // Inline styles
    const styles = {
        container: {
            fontFamily: 'Arial, sans-serif',
            maxWidth: '600px',
            maxHeight: '1080px',
            margin: '0 auto',
            padding: '20px',
            backgroundColor: '#f5f5f5',
            borderRadius: '8px',
            boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
            minHeight: '400px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between'
        },
        form: {
            display: 'flex',
            borderTop: '1px solid #ddd'
        },
        input: {
            flex: 1,
            padding: '10px',
            fontSize: '16px',
            border: 'none',
            outline: 'none'
        },
        button: {
            padding: '10px 20px',
            fontSize: '16px',
            border: 'none',
            backgroundColor: '#007BFF',
            color: 'white',
            cursor: 'pointer'
        },
        messages: {
            flex: 1,
            overflowY: 'scroll',
        },
        message: {
            margin: '5px 0',
            padding: '10px',
            borderRadius: '5px',
            backgroundColor: '#e0e0e0'
        },
        userMessage: {
            textAlign: 'right',
            backgroundColor: '#007BFF',
            color: 'white'
        }
    };

    return (
        <div style={styles.container}>
            <h1>IT Support Chatbot</h1>
                <div style={styles.messages}>
                    {responses.map((exchange, index) => (
                        <p key={index}>
                            <p style={{fontWeight:'bold'}}>You</p>
                            <p>
                                {exchange.query} <br />
                            </p> 
                            <div style={{textAlign: 'end'}}>
                                <p style={{fontWeight:'bold'}}>Chatbot</p>
                                <p>
                                    <TypeAnimation
                                        sequence={[exchange.reply, 1000]}
                                        speed={50}
                                    /><br /> 
                                </p> 
                            </div>
                        </p>
                    ))}
                </div>  
                <div>
                </div> 
            
            <form onSubmit={handleSubmit} style={styles.form}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Describe your IT issue..."
                    style={styles.input}
                />
                <button type="submit" style={styles.button}>Send</button>
            </form>
           
        </div>
    );
}

export default Chatbot;

