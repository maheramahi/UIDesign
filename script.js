const startBtn = document.getElementById("start-btn");
const instruction = document.getElementById("instruction");
const response = document.getElementById("response");
const actionButtons = document.querySelectorAll(".action-btn");

const synth = window.speechSynthesis;
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";
recognition.interimResults = false;

function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    synth.speak(utterance);
}

function processCommand(command) {
    response.style.display = "block";

    if (command.includes("time")) {
        const time = new Date().toLocaleTimeString();
        speak(`The current time is ${time}`);
        response.textContent = `The current time is ${time}.`;
    } else if (command.includes("date")) {
        const date = new Date().toLocaleDateString();
        speak(`Today's date is ${date}`);
        response.textContent = `Today's date is ${date}.`;
    } else if (command.includes("joke")) {
        const jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don’t skeletons fight each other? They don’t have the guts."
        ];
        const joke = jokes[Math.floor(Math.random() * jokes.length)];
        speak(joke);
        response.textContent = joke;
    } else if (command.includes("weather")) {
        fetchWeather();
    } else {
        speak("I did not understand that. Please try again.");
        response.textContent = "I did not understand that. Please try again.";
    }
}

function fetchWeather() {
    const apiKey = "your_openweather_api_key"; // Replace with your actual API key
    const city = "your_city"; // Replace with your actual city
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

    fetch(url)
        .then(res => res.json())
        .then(data => {
            if (data.cod === 200) {
                const weather = `The current temperature in ${data.name} is ${data.main.temp}°C with ${data.weather[0].description}.`;
                speak(weather);
                response.textContent = weather;
            } else {
                speak("Unable to fetch weather information. Please check the city name or API key.");
                response.textContent = "Unable to fetch weather information. Please check the city name or API key.";
            }
        })
        .catch(() => {
            speak("I couldn't fetch the weather information right now.");
            response.textContent = "I couldn't fetch the weather information right now.";
        });
}

startBtn.addEventListener("click", () => {
    instruction.textContent = "Listening...";
    recognition.start();
});

recognition.onresult = event => {
    const command = event.results[0][0].transcript.toLowerCase();
    instruction.textContent = `You said: "${command}"`;
    processCommand(command);
};

recognition.onerror = event => {
    speak("I couldn't hear anything. Please try again.");
    instruction.textContent = `Error: ${event.error}`;
};

actionButtons.forEach(button => {
    button.addEventListener("click", () => {
        const command = button.dataset.command;
        instruction.textContent = `You clicked: "${command}"`;
        processCommand(command);
    });
});
