document.getElementById('findPrices').addEventListener('click', () => {
    console.log("hello from popup.js file")
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { action: "findPrices" });
    });
});

