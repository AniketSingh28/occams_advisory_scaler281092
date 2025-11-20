// frontend/app.js

const chatEl = document.getElementById('chat');
const input = document.getElementById('input');

let sessionId = 'sess_' + Math.random().toString(36).slice(2, 9);
let onboarding = { name: null, email: null, phone: null };
let nudgeCount = 0;

function append(role, text) {
    const d = document.createElement('div');
    d.className = 'msg ' + (role === 'bot' ? 'bot' : 'user');
    d.innerText = text;
    chatEl.appendChild(d);
    chatEl.scrollTop = chatEl.scrollHeight;
}

async function sendMessage(msg) {
    append('user', msg);

    // simple onboarding flow: if name missing ask
    if (!onboarding.name) {
        append('bot', 'Hi! Before we start, may I have your name?');
        onboarding.name = 'asked';
        return;
    }

    // if name asked and user typed something assume it's name
    if (onboarding.name === 'asked') {
        onboarding.name = msg;
        append('bot', `Nice to meet you, ${msg}. What's your email?`);
        return;
    }
}
