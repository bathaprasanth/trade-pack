const searchBtn = document.getElementById('searchBtn');
const sectorInput = document.getElementById('sectorInput');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const reportContent = document.getElementById('reportContent');
const errorMessage = document.getElementById('errorMessage');
const timerContainer = document.getElementById('timerContainer');
const countdownEl = document.getElementById('countdown');
const timerBar = document.getElementById('timerBar');

const API_Base = ""; // Relative path

searchBtn.addEventListener('click', handleSearch);
sectorInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSearch();
});

async function handleSearch() {
    const sector = sectorInput.value.trim();
    if (!sector) return;

    // Reset UI
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    setLoading(true);

    try {
        const response = await fetch(`/analyze/${encodeURIComponent(sector)}`, {
            headers: {
                'X-API-Key': 'gemini-trade-api'
            }
        });

        const data = await response.json();

        if (response.ok) {
            // Success
            renderReport(data.analysis_report);
        } else if (response.status === 429) {
            // Rate Limited
            showError("We are experiencing high traffic (Quota Exceeded). Please wait.", true);
        } else {
            // Other Error
            const msg = data.detail || "An unexpected error occurred.";
            showError(msg);
        }

    } catch (err) {
        showError("Failed to connect to the server. Is it running?");
        console.error(err);
    } finally {
        setLoading(false);
    }
}

function setLoading(isLoading) {
    searchBtn.disabled = isLoading;
    if (isLoading) {
        document.querySelector('.btn-text').classList.add('hidden');
        loadingSpinner.classList.remove('hidden');
    } else {
        document.querySelector('.btn-text').classList.remove('hidden');
        loadingSpinner.classList.add('hidden');
    }
}

function renderReport(markdownText) {
    if (!markdownText) {
        showError("Received empty analysis.");
        return;
    }
    // Parse Markdown using marked.js
    reportContent.innerHTML = marked.parse(markdownText);
    resultsSection.classList.remove('hidden');
}

function showError(message, isRateLimit = false) {
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');

    if (isRateLimit) {
        startTimer(60); // 60 seconds wait
    } else {
        timerContainer.classList.add('hidden');
    }
}

function startTimer(seconds) {
    timerContainer.classList.remove('hidden');
    let timeLeft = seconds;
    countdownEl.textContent = timeLeft;
    timerBar.style.width = '100%';

    const interval = setInterval(() => {
        timeLeft--;
        countdownEl.textContent = timeLeft;
        const percentage = (timeLeft / seconds) * 100;
        timerBar.style.width = `${percentage}%`;

        if (timeLeft <= 0) {
            clearInterval(interval);
            timerContainer.classList.add('hidden');
            errorMessage.textContent = "You can try again now!";
            timerBar.style.width = '0%';
        }
    }, 1000);
}
