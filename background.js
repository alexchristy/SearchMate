// // background.js

// // Function to set data in chrome.storage.local
// function setDataInStorage(data) {
//     chrome.storage.local.set({ myData: data }, function() {
//         console.log('Data set in local storage:', data);
        
//         // Now, let's set a cookie with the data
//         setCookie('myCookie', JSON.stringify(data), 1);
//     });
// }

// // Function to set a cookie
// function setCookie(name, value, expirationDays) {
//     const expirationDate = new Date();
//     expirationDate.setDate(expirationDate.getDate() + expirationDays);

//     chrome.cookies.set({
//         url: 'http://your-extension-url/', // Replace with your extension's URL
//         name: name,
//         value: value,
//         expirationDate: expirationDate.getTime() / 1000, // Convert to seconds
//     }, function(cookie) {
//         console.log('Cookie set:', cookie);
//     });
// }

// // Example: Set data in storage and then set a cookie
// setDataInStorage({ key: 'value' });
