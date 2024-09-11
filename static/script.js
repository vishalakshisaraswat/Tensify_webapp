// Handle form submission
document.getElementById('tenseForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from submitting normally

    const sentence = document.getElementById('sentenceInput').value;
    
    // Send POST request to the backend
    fetch('/detect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `sentence=${encodeURIComponent(sentence)}`,
    })
    .then(response => response.json())
    .then(data => {
        // Display the tense result on the page
        document.getElementById('result').innerText = data.result;
    })
    .catch(error => console.error('Error:', error));
});


