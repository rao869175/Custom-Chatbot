function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return;

    let chatLog = document.getElementById("chat-log");
    chatLog.innerHTML += `<div class="user">You: ${userInput}</div>`;

    fetch("/get_response", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `user_message=${encodeURIComponent(userInput)}`
    })
    .then(response => response.json())
    .then(data => {
        chatLog.innerHTML += `<div class="bot">Bot: ${data.bot_reply}</div>`;
        document.getElementById("user-input").value = "";
        chatLog.scrollTop = chatLog.scrollHeight;
    });
}

// 📌 Listen for Enter key
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});
