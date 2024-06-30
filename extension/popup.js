document.addEventListener('DOMContentLoaded', function() {
    const sourceLang = document.getElementById('sourceLang');
    const targetLang = document.getElementById('targetLang');
  
    // Load saved settings
    chrome.storage.sync.get(['sourceLang', 'targetLang'], function(result) {
      if (result.sourceLang) sourceLang.value = result.sourceLang;
      if (result.targetLang) targetLang.value = result.targetLang;
    });
  
    // Save settings when changed
    sourceLang.addEventListener('change', function() {
      chrome.storage.sync.set({sourceLang: sourceLang.value});
    });
  
    targetLang.addEventListener('change', function() {
      chrome.storage.sync.set({targetLang: targetLang.value});
    });
  });