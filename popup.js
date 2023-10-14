// popup.js

document.addEventListener('DOMContentLoaded', function () {
    const urlContainer = document.getElementById('urlContainer');

    // Get the active tab's URL
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const currentTab = tabs[0];
        const url = currentTab.url;

        // Display the URL in your popup
        urlContainer.textContent = `Current URL: ${url}`;
    });
});


document.addEventListener('DOMContentLoaded', function () {
    // Get references to the input field and the send button
    const messageInput = document.getElementById('messageInput');
    const sendMessageButton = document.getElementById('sendMessageButton');
const urlContainer = document.getElementById('urlContainer');

    try {
        loadMessages();
    }
    catch (error) {}
    
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

    function loadMessages() {
        chrome.storage.local.get(['chatMessages'], function(result) {
            const chatMessages = result.chatMessages || [];
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
        saveMessage(messageElement.textContent);
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

    function saveMessage(message) {
        chrome.storage.local.get(['chatMessages'], function(result) {
            const chatMessages = result.chatMessages || [];
            chatMessages.push(message);
    
            // Save the updated messages to storage
            chrome.storage.local.set({ chatMessages: chatMessages });
        });
    }
});

