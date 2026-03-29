async function searchCourses() {
    const query = document.getElementById('query').value.trim();
    const price = document.getElementById('price').value;
    const level = document.getElementById('level').value;

    // ✅ STOP empty search
    if (!query) {
        alert("Please enter a skill or career goal");
        return;
    }
    if (!query) {
    document.getElementById('results').innerHTML =
        "<p>Please enter a skill to search</p>";
    return;
    }
    try {
        const res = await fetch(`/search?query=${query}&price=${price}&level=${level}`);
        const data = await res.json();

        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '';

        if (data.error) {
            resultsDiv.innerHTML = `<p>${data.error}</p>`;
            return;
        }

        data.forEach(course => {
            const card = document.createElement('div');
            card.className = 'card';

            card.innerHTML = `
                <h3>${course.title}</h3>
                <p>Rating: ${course.rating}</p>
                <p>Price: ${course.price}</p>
                <a href="${course.url}" target="_blank">View Course</a>
            `;

            resultsDiv.appendChild(card);
        });

    } catch (error) {
        console.error(error);
        alert("Something went wrong");
    }
}