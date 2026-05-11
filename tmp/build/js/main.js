// Enhanced JavaScript for Hyunsoo Han's Personal Website Calendar
// This handles calendar functionality with localStorage and enhanced UX

let calendarContainer = null;

document.addEventListener('DOMContentLoaded', function() {
    // Calendar functionality
    calendarContainer = document.querySelector('.calendar-container');

    if (calendarContainer) {
        initializeCalendar();
    }

    // Initialize event handling
    initializeEventHandling();

    // Load existing events
    loadEvents();
});

function initializeCalendar() {
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth();

    // Create calendar header
    const calendarHeader = document.createElement('div');
    calendarHeader.className = 'calendar-header';
    calendarHeader.textContent = `${year}년 ${month + 1}월`;

    // Create calendar grid
    const calendarGrid = document.createElement('div');
    calendarGrid.className = 'calendar-grid';

    // Add day headers
    const dayHeaders = ['일', '월', '화', '수', '목', '금', '토'];
    dayHeaders.forEach(day => {
        const header = document.createElement('div');
        header.className = 'calendar-header';
        header.textContent = day;
        calendarGrid.appendChild(header);
    });

    // Get days in month and first day of month
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const firstDayOfMonth = new Date(year, month, 1).getDay();

    // Add empty cells for days before the first day
    for (let i = 0; i < firstDayOfMonth; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.className = 'calendar-day other-month';
        calendarGrid.appendChild(emptyCell);
    }

    // Add cells for each day
    for (let day = 1; day <= daysInMonth; day++) {
        const dayCell = document.createElement('div');
        dayCell.className = 'calendar-day';
        const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        dayCell.setAttribute('data-date', dateStr);

        // Highlight today
        if (isToday(year, month, day)) {
            dayCell.classList.add('today');
        }

        dayCell.innerHTML = `<div class="day-number">${day}</div>`;

        // Check if this day has events
        const events = getEventsForDate(dateStr);
        if (events.length > 0) {
            dayCell.classList.add('has-events');
        }

        // Add click event to show events
        dayCell.addEventListener('click', function() {
            showEventsForDate(dateStr);
        });

        calendarGrid.appendChild(dayCell);
    }

    // Add calendar to container
    calendarContainer.appendChild(calendarHeader);
    calendarContainer.appendChild(calendarGrid);

    // Add event form
    addEventForm();
}

function isToday(year, month, day) {
    const today = new Date();
    return today.getFullYear() === year &&
           today.getMonth() === month &&
           today.getDate() === day;
}

function addEventForm() {
    const form = document.createElement('div');
    form.className = 'add-event-form';
    form.innerHTML = `
        <h3>Add Event</h3>
        <input type="text" id="event-input" class="event-input" placeholder="Event title" required>
        <textarea id="event-description" class="event-input" placeholder="Event description"></textarea>
        <button type="button" onclick="saveEvent()" class="event-button">Save Event</button>
    `;
    calendarContainer.appendChild(form);
}

function saveEvent() {
    const eventInput = document.getElementById('event-input');
    const descriptionInput = document.getElementById('event-description');
    const date = getCurrentSelectedDate();

    if (!date || !eventInput.value.trim()) {
        alert('Please select a date and enter an event title');
        return;
    }

    const event = {
        title: eventInput.value.trim(),
        description: descriptionInput.value.trim(),
        date: date,
        timestamp: new Date().toISOString()
    };

    const events = getEventsForDate(date);
    events.push(event);

    localStorage.setItem(`events_${date}`, JSON.stringify(events));

    // Clear form
    eventInput.value = '';
    descriptionInput.value = '';

    // Refresh calendar
    refreshCalendar();

    alert('Event saved successfully!');
}

function getEventsForDate(date) {
    const storedEvents = localStorage.getItem(`events_${date}`);
    try {
        return storedEvents ? JSON.parse(storedEvents) : [];
    } catch (e) {
        return [];
    }
}

function loadEvents() {
    // This would load events when the page loads
    // Calendar initialization handles this through the grid creation
}

function showEventsForDate(date) {
    const events = getEventsForDate(date);

    if (events.length === 0) {
        alert('No events for this date');
        return;
    }

    let eventList = `Events for ${date}:\n\n`;
    events.forEach(event => {
        eventList += `• ${event.title}\n`;
        if (event.description) {
            eventList += `  ${event.description}\n`;
        }
        eventList += '\n';
    });

    alert(eventList);
}

function refreshCalendar() {
    // Reload the page to refresh calendar
    location.reload();
}

function getCurrentSelectedDate() {
    // In a real implementation, this would return the selected date
    // For now, we'll use today's date
    const today = new Date();
    return `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
}

function initializeEventHandling() {
    // Handle form submission via enter key
    const eventInput = document.getElementById('event-input');
    const descriptionInput = document.getElementById('event-description');

    if (eventInput) {
        eventInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                saveEvent();
            }
        });
    }

    if (descriptionInput) {
        descriptionInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                saveEvent();
            }
        });
    }
}