window.onload = function () {
    appendMessage("bot", "👋 Hello! I am NTPC HR Assistant.");
    appendMessage("bot", "How may I help you today?");
};

function send() {
    const msg = document.getElementById("user_input").value.trim();
    if (!msg) return;

    appendMessage("user", msg);

    // Bot typing animation
    const typingDiv = appendMessage("bot", "", true, true);

    fetch("/get", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: "msg=" + encodeURIComponent(msg)
    })
    .then(res => res.json())
    .then(data => {
        typingDiv.remove();
        appendMessage("bot", data.response);
        document.getElementById("user_input").value = "";

        // ✅ Bot speaks the response
        speakText(data.response);
    });
}

function sendQuick(msg) {
    document.getElementById("user_input").value = msg;
    send();
}

function appendMessage(sender, msg, isTyping = false, typingOnly = false) {
    const wrapper = document.createElement("div");
    wrapper.className = "message-wrapper " + sender;

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = sender === "bot" ? "🤖" : "🙂";
    wrapper.appendChild(avatar);

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    if (typingOnly) {
        bubble.innerHTML = "<span class='dot'></span><span class='dot'></span><span class='dot'></span>";
    } else {
        bubble.textContent = msg;
    }

    wrapper.appendChild(bubble);
    document.getElementById("chatlog").appendChild(wrapper);
    document.getElementById("chatlog").scrollTop = document.getElementById("chatlog").scrollHeight;

    return wrapper;
}

function clearChat() {
    document.getElementById("chatlog").innerHTML = "";
    fetch("/clear", { method: "POST" });
}

// ✅ Voice Input (Speech Recognition)
function startVoice() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-IN'; // Change to 'hi-IN' for Hindi
    recognition.start();

    recognition.onresult = function (event) {
        const voiceText = event.results[0][0].transcript;
        console.log("🎤 Voice input:", voiceText);
        document.getElementById("user_input").value = voiceText;
        send(); // Auto-send voice message
    };

    recognition.onerror = function (event) {
        console.error("❌ Voice recognition error:", event.error);
        alert("Voice error: " + event.error);
    };
}

// ✅ Text-to-Speech (Bot talks back)
function speakText(text) {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-IN'; // Use 'hi-IN' if reply is in Hindi
    utterance.pitch = 1;
    utterance.rate = 1;
    synth.speak(utterance);
}
