function showTranslationStatus(message) {
  console.log('Status:', message);
  let statusDiv = document.getElementById('translation-status');
  if (!statusDiv) {
    statusDiv = document.createElement('div');
    statusDiv.id = 'translation-status';
    statusDiv.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      padding: 10px;
      background-color: #f0f0f0;
      border: 1px solid #ccc;
      border-radius: 5px;
      z-index: 10000;
    `;
    document.body.appendChild(statusDiv);
  }
  statusDiv.textContent = message;
}

function showTranslationResult(translation) {
  console.log('Showing translation result:', translation);
  const resultDiv = document.createElement('div');
  resultDiv.id = 'translation-result';
  resultDiv.style.cssText = `
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 20px;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    z-index: 10001;
    max-width: 80%;
    max-height: 80%;
    overflow: auto;
  `;
  resultDiv.innerHTML = `
    <h3>Translation:</h3>
    <p>${translation}</p>
    <button id="close-translation">Close</button>
  `;
  document.body.appendChild(resultDiv);

  document.getElementById('close-translation').addEventListener('click', () => {
    document.body.removeChild(resultDiv);
    const statusDiv = document.getElementById('translation-status');
    if (statusDiv) document.body.removeChild(statusDiv);
  });
}

function translateText(text) {
  console.log('Translating text:', text);
  chrome.storage.sync.get(['sourceLang', 'targetLang'], function(result) {
    const sourceLang = result.sourceLang || 'eng_Latn';
    const targetLang = result.targetLang || 'hin_Deva';
    console.log('Source language:', sourceLang, 'Target language:', targetLang);

    showTranslationStatus('Translating...');

    fetch('http://localhost:5000/translate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: text,
        source_lang: sourceLang,
        target_lang: targetLang
      }),
    })
    .then(response => {
      console.log('Received response:', response);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('Received data:', data);
      if (data && data.translation) {
        showTranslationResult(data.translation);
      } else {
        throw new Error('Invalid response from server');
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      let errorMessage = 'Translation error occurred. ';
      if (error.message.includes('Failed to fetch')) {
        errorMessage += 'Unable to connect to the server. Please check if the server is running at http://localhost:5000.';
      } else {
        errorMessage += error.message;
      }
      showTranslationStatus(errorMessage);
    });
  });
}

// Ensure the content script is injected and running
console.log('Content script loaded and running');

// Add a listener for messages from the background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Received message:', request);
  if (request.action === "translate") {
    translateText(request.text);
  }
});