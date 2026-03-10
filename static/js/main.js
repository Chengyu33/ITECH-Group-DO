// Wait until the entire webpage's HTML is fully loaded before executing
document.addEventListener("DOMContentLoaded", function() {
    
    // Find the form we named in login.html (id="auth-form")
    const authForm = document.getElementById("auth-form");

    // Check if the current page actually has this form (because this JS also loads on the homepage)
    if (authForm) {
        authForm.addEventListener("submit", function(event) {
            
            // Extract the text entered by the user in the email and password fields
            const emailValue = document.getElementById("emailInput").value.trim();
            const passwordValue = document.getElementById("passwordInput").value.trim();

            // If the email is empty, or the password is empty
            if (emailValue === "" || passwordValue === "") {
                event.preventDefault(); 
                alert("Please fill in the complete email and password!");
            } 
            else {
                // After Yonghui has set up the backend database, we will delete the following two lines so that it can submit normally.
                event.preventDefault();
                alert("Frontend validation passed, ready to call the backend server");
            }
        });
    }
});