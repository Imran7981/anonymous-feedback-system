document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
  
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const errorMsg = document.getElementById('errorMsg');
  
    if (!username || !password) {
      errorMsg.textContent = "Both fields are required.";
      return;
    }
  
    if (password.length < 4) {
      errorMsg.textContent = "Password must be at least 4 characters.";
      return;
    }
  
    // Simulate login success
    alert(`Welcome, ${username}! You're now logged in anonymously.`);
    errorMsg.textContent = "";
    document.getElementById('loginForm').reset(); // Clear the form
    window.location.href = 'index.html'; // Redirect to home page
  });
  