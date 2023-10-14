// popup.js

document.addEventListener('DOMContentLoaded', function () {
    // Get references to the input field and the send button
    const messageInput = document.getElementById('messageInput');
    const sendMessageButton = document.getElementById('sendMessageButton');

    // Add a click event listener to the send button
    sendMessageButton.addEventListener('click', function () {
        // Get the message from the input field
        const message = messageInput.value;

        // Do something with the message (e.g., send it or display it)
        if (message.trim() !== '') {
            // For demonstration, let's display the message in the chat messages container
            displayMessage('You', message);

            // Clear the input field
            messageInput.value = '';
        }
    });

    // Function to display a message in the chat messages container
    function displayMessage(sender, message) {
        const chatMessages = document.getElementById('chatMessages');
        const messageElement = document.createElement('div');
        messageElement.textContent = sender + ': ' + message;
        chatMessages.appendChild(messageElement);
    }
});

