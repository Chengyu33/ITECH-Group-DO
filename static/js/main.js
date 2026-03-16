// Wait until the entire webpage's HTML is fully loaded before executing
document.addEventListener("DOMContentLoaded", function() {
    
    // Find the form we named in login.html (id="auth-form")
    const authForm = document.getElementById("auth-form");
    
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
                .then(response => response.json())
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
                        const cardHtml = `
                            <div class="col">
                                <div class="card h-100 border-0 shadow-sm rounded-4">
                                    <img src="${event.image}" class="card-img-top rounded-top-4" alt="Event Poster" style="height: 200px; object-fit: cover;">
                                    
                                    <div class="card-body">
                                        <span class="badge bg-primary mb-2">${event.category || 'General'}</span>
    
                                        <h5 class="card-title fw-bold">${event.title}</h5>
                                        <p class="card-text text-muted mb-1">📅 Time：${event.date_time}</p>
                                        <p class="card-text text-muted">📍 Location：${event.location}</p>
                                        <p class="card-text text-primary fw-bold mb-2">👥 Registered: ${event.registered_count || 0} / 50 (Capacity)</p>
                                        <p class="card-text mt-2">${event.description}</p>
                                    </div>
                                    
                                    <div class="card-footer bg-white border-0 pb-3 pt-0">
                                        <a href="/event/${event.id}/" class="btn btn-outline-dark w-100 rounded-pill fw-bold">View Details / Register</a>
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