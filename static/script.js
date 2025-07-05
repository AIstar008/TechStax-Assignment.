async function fetchEvents() {
  try {
    const res = await axios.get('/events');
    const container = document.getElementById('events-container');
    container.innerHTML = '';

    res.data.forEach(event => {
      let msg = '';
      if (event.action === "push") {
        msg = `"${event.author}" pushed to "${event.to_branch}" on ${event.timestamp}`;
      } else if (event.action === "pull_request") {
        msg = `"${event.author}" submitted a pull request from "${event.from_branch}" to "${event.to_branch}" on ${event.timestamp}`;
      } else if (event.action === "merge") {
        msg = `"${event.author}" merged branch "${event.from_branch}" to "${event.to_branch}" on ${event.timestamp}`;
      }

      const div = document.createElement('div');
      div.className = 'event';
      div.innerText = msg;
      container.appendChild(div);
    });

  } catch (err) {
    console.error('Error fetching events', err);
  }
}

fetchEvents();
setInterval(fetchEvents, 15000);
