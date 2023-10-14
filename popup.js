// popup.js

document.addEventListener('DOMContentLoaded', function () {
    // Get references to the input field and the send button
    const messageInput = document.getElementById('messageInput');
    const sendMessageButton = document.getElementById('sendMessageButton');
    const urlContainer = document.getElementById('urlContainer');

    // Get the active tab's URL
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const currentTab = tabs[0];
        const url = currentTab.url;
    
        // Display the URL in your popup
        urlContainer.textContent = url;
    });
    function getRootUrl(url) {
        const parser = document.createElement('a');
        parser.href = urlContainer.textContent;

        // Combine the protocol, hostname, and port to get the root URL
        return parser.protocol + '//' + parser.hostname;
    }

    const rootUrl = getRootUrl(urlContainer.textContent);
    console.log(rootUrl);

    try {
        loadMessages(rootUrl);
    }
    catch (error) {
        console.log(error);
    }
    
    // Add a click event listener to the send button
    sendMessageButton.addEventListener('click', function () {
        sendMessage();
    });

    // Add a key press event listener to the input field
    messageInput.addEventListener('keyup', function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    function loadMessages(url) {
        chrome.storage.local.get(url, function(result) {
            const chatMessages = result[url] || [];
            displaySavedMessages(chatMessages);
        });
    }

    function sendMessage() {
        const message = messageInput.value;

        if (message.trim() !== '') {
            displayMessage('You', message);
            messageInput.value = '';
        }
    }

    // Function to display a message in the chat messages container and then save to local storage
    function displayMessage(sender, message) {
        const chatMessages = document.getElementById('chatMessages');
        const messageElement = document.createElement('div');
        messageElement.textContent = sender + ': ' + message;
        chatMessages.appendChild(messageElement);
        saveMessage(rootUrl, messageElement.textContent);
    }

    // Function to load saved messages when popup is repopend
    function displaySavedMessages(messages) {
        const chatDiv = document.getElementById('chatMessages');
        chatDiv.innerHTML = ''; // Clear existing messages
    
        messages.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.textContent = message;
            console.log(message);
            chatDiv.appendChild(messageElement);
        });
    }

    function saveMessage(url, message) {
        chrome.storage.local.get(url, function(result) {
            const chatMessages = result[url] || [];
            chatMessages.push(message);
    
            const data = {};
            data[url] = chatMessages;

            chrome.storage.local.set(data, function() {
                console.log('Chat message saved to chrome.storage.local:', data);
            });
        });
    }
});

