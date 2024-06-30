chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
      id: "translateText",
      title: "Translate selected text",
      contexts: ["selection"]
    });
  });
  
  chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "translateText") {
      chrome.tabs.sendMessage(tab.id, {action: "translate", text: info.selectionText});
    }
  });