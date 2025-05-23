let localDisplay = document.getElementById("localDisplay"); // container for feedback display

function createFeedbackEntry(feedbackText, fileName = "") {
    const entryDiv = document.createElement("div");
    entryDiv.classList.add("feedback-entry");

    // Feedback text
    const feedbackPara = document.createElement("p");
    feedbackPara.innerText = "📝 " + feedbackText;
    entryDiv.appendChild(feedbackPara);

    // File name (if any)
    if (fileName) {
        const filePara = document.createElement("p");
        filePara.innerText = "📎 File: " + fileName;
        entryDiv.appendChild(filePara);
    }

    // Delete button
    const deleteBtn = document.createElement("button");
    deleteBtn.innerText = "Delete ❌";
    deleteBtn.classList.add("delete-btn");
    deleteBtn.onclick = () => entryDiv.remove();
    entryDiv.appendChild(deleteBtn);

    localDisplay.appendChild(entryDiv);
}

// Call this function inside submitFeedback success block
function submitFeedback() {
    let feedback = feedbackInput.value;
    let file = fileInput.files[0];

    if (feedback.trim() === "" && !file) {
        message.innerText = "Please provide feedback or upload a file!";
        message.style.color = "red";
        return;
    }

    let formData = new FormData();
    formData.append("feedback", feedback);
    if (file) {
        formData.append("file", file);
    }

    fetch("http://localhost:3000/submit", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        console.log("Server response:", data);
        message.innerText = "Feedback submitted successfully!";
        message.style.color = "green";

        // ✅ Add entry to local display
        createFeedbackEntry(feedback, file ? file.name : "");

        // Clear form
        feedbackInput.value = "";
        fileInput.value = "";
        previewImage.style.display = "none";
    })
    .catch(error => {
        console.error("Error:", error);
        message.innerText = "Error submitting feedback.";
        message.style.color = "red";
    });
}
