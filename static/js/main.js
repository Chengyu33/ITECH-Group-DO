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

    // Dynamic Search Interaction
    const searchInput = document.getElementById("searchInput");
    const eventContainer = document.getElementById("eventContainer");

    // Execute this logic only if the search input and container exist on the current page
    if (searchInput && eventContainer) {
        searchInput.addEventListener("keyup", function() {
            // Get input value and strip whitespace
            const query = searchInput.value.trim();

            // Initiate AJAX request to fetch filtered data from backend
            fetch(`/api/search/?q=${encodeURIComponent(query)}`)
                .then(response => response.json()) // 把后端返回的数据转换成 JSON 格式
                .then(data => {
                    // Clear existing event cards from the container
                    eventContainer.innerHTML = "";

                    // Handle 'no results found' state
                    if (data.events.length === 0) {
                        eventContainer.innerHTML = "<div class='col-12 text-center text-muted mt-5'><p>No events found matching your search.</p></div>";
                        return;
                    }

                    // Iterate through results and dynamically inject HTML cards
                    data.events.forEach(event => {
                        // 这里的 HTML 结构必须和 Xiangyu 在 Events.html 里写的一模一样
                        const cardHtml = `
                            <div class="col">
                                <div class="card h-100 border-0 shadow-sm rounded-4">
                                    <img src="${event.image}" class="card-img-top rounded-top-4" alt="Event Poster" style="height: 200px; object-fit: cover;">
                                    
                                    <div class="card-body">
                                        <h5 class="card-title fw-bold">${event.title}</h5>
                                        <p class="card-text text-muted mb-1">📅 Time：${event.date_time}</p>
                                        <p class="card-text text-muted">📍 Location：${event.location}</p>
                                        <p class="card-text mt-2">${event.description}</p>
                                    </div>
                                    
                                    <div class="card-footer bg-white border-0 pb-3 pt-0">
                                        <a href="#" class="btn btn-outline-dark w-100 rounded-pill fw-bold">View Details / Register</a>
                                    </div>
                                </div>
                            </div>
                        `;
                        // Append the constructed HTML to the container
                        eventContainer.insertAdjacentHTML('beforeend', cardHtml);
                    });
                })
                .catch(error => {
                    console.error("AJAX Error:", error);
                });
        });
    }
});