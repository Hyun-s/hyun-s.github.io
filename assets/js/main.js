// Enhanced JavaScript for Hyunsoo Han's Personal Website Calendar
// This handles calendar functionality with localStorage and enhanced UX

// Global calendar container reference
let calendarContainer = null;

function initCalendar() {
    // Always re-query for the container in case it wasn't available before
    calendarContainer = document.querySelector('.calendar-container');

    if (calendarContainer) {
        initializeCalendar();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Load existing events
    loadEvents();

    // Initialize calendar
    initCalendar();
});

// Global calendar state
let currentYear = null;
let currentMonth = null;

// Load persisted month state if available
function loadCalendarState() {
    try {
        const savedState = localStorage.getItem('calendar_view_state');
        if (savedState) {
            const state = JSON.parse(savedState);
            if (state.year && state.month !== null) {
                currentYear = state.year;
                currentMonth = state.month;
                return true;
            }
        }
    } catch (e) {
        // Ignore parse errors
    }
    return false;
}

function saveCalendarState() {
    try {
        localStorage.setItem('calendar_view_state', JSON.stringify({
            year: currentYear,
            month: currentMonth
        }));
    } catch (e) {
        // Ignore save errors
    }
}

function initializeCalendar() {
    // Load persisted state or use current date
    if (!loadCalendarState()) {
        const today = new Date();
        currentYear = today.getFullYear();
        currentMonth = today.getMonth();
    }

    // Create calendar header container
    const calendarHeader = document.createElement('div');
    calendarHeader.className = 'calendar-header';

    // Create navigation controls
    const navContainer = document.createElement('div');
    navContainer.className = 'calendar-nav';

    const prevBtn = document.createElement('button');
    prevBtn.className = 'calendar-nav-btn prev';
    prevBtn.textContent = '<';
    prevBtn.setAttribute('aria-label', 'Previous month');

    const nextBtn = document.createElement('button');
    nextBtn.className = 'calendar-nav-btn next';
    nextBtn.textContent = '>';
    nextBtn.setAttribute('aria-label', 'Next month');

    navContainer.appendChild(prevBtn);
    navContainer.appendChild(nextBtn);

    // Month display
    const monthDisplay = document.createElement('div');
    monthDisplay.className = 'calendar-month-display';
    monthDisplay.textContent = `${currentYear}년 ${currentMonth + 1}월`;

    calendarHeader.appendChild(prevBtn);
    calendarHeader.appendChild(monthDisplay);
    calendarHeader.appendChild(nextBtn);

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
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();

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
        const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        dayCell.setAttribute('data-date', dateStr);

        // Highlight today
        if (isToday(currentYear, currentMonth, day)) {
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

    // Add navigation event listeners
    prevBtn.addEventListener('click', function() {
        changeMonth(-1);
    });
    nextBtn.addEventListener('click', function() {
        changeMonth(1);
    });
}

function changeMonth(direction) {
    currentMonth += direction;

    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    } else if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }

    saveCalendarState();
    refreshCalendar();
}

function getSelectedDate() {
    if (currentYear === null || currentMonth === null) {
        const today = new Date();
        return `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
    }
    return `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(getCurrentDay()).padStart(2, '0')}`;
}

function getCurrentDay() {
    const today = new Date();
    return today.getDate();
}

function isToday(year, month, day) {
    const today = new Date();
    return today.getFullYear() === year &&
           today.getMonth() === month &&
           today.getDate() === day;
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
    const formattedDate = formatDateDisplay(date);

    // Create the combined dialog content
    const dialogContent = document.createElement('div');
    dialogContent.className = 'date-dialog-content';

    // Date header
    const dateHeader = document.createElement('h3');
    dateHeader.className = 'date-dialog-header';
    dateHeader.textContent = formattedDate;
    dialogContent.appendChild(dateHeader);

    // Event list container
    const eventListContainer = document.createElement('div');
    eventListContainer.className = 'date-dialog-event-list';
    dialogContent.appendChild(eventListContainer);

    // Add event form container
    const addFormContainer = document.createElement('div');
    addFormContainer.className = 'date-dialog-add-form';
    dialogContent.appendChild(addFormContainer);

    // Show modal first
    const modal = showInlineModal('', '', dialogContent);

    // Render events and form
    renderEventListAndForm(date, events, eventListContainer, addFormContainer);
}

function renderEventListAndForm(date, events, eventListContainer, addFormContainer) {
    // Clear existing content
    eventListContainer.innerHTML = '';
    addFormContainer.innerHTML = '';

    // Render event list
    if (events.length === 0) {
        const noEventsMsg = document.createElement('p');
        noEventsMsg.className = 'no-events-message';
        noEventsMsg.textContent = 'No events for this date';
        eventListContainer.appendChild(noEventsMsg);
    } else {
        events.forEach((event, index) => {
            const eventItem = createEventItem(date, event, index);
            eventListContainer.appendChild(eventItem);
        });
    }

    // Render add form
    const form = createAddEventForm(date);
    addFormContainer.appendChild(form);
}

function createEventItem(date, event, index) {
    const eventItem = document.createElement('div');
    eventItem.className = 'event-item';
    eventItem.dataset.index = index;

    const titleDiv = document.createElement('div');
    titleDiv.className = 'event-title';
    titleDiv.textContent = event.title;
    titleDiv.style.cursor = 'pointer';
    titleDiv.addEventListener('click', () => toggleEventDetails(eventItem, date, index));
    eventItem.appendChild(titleDiv);

    // Details container (hidden by default)
    const detailsDiv = document.createElement('div');
    detailsDiv.className = 'event-details';
    detailsDiv.style.display = 'none';
    eventItem.appendChild(detailsDiv);

    eventListContainer.appendChild(eventItem);

    return eventItem;
}

function toggleEventDetails(eventItem, date, index) {
    const details = eventItem.querySelector('.event-details');
    const isExpanded = details.style.display !== 'none';

    // Close all other expanded items
    document.querySelectorAll('.event-details').forEach(el => {
        el.style.display = 'none';
    });

    if (!isExpanded) {
        // Show details for this event
        const event = getEventsForDate(date)[index];
        details.innerHTML = `
            <div class="event-description">${escapeHtml(event.description || '')}</div>
            <div class="event-time">${formatTime(event.startTime || '')} ${event.endTime ? '- ' + formatTime(event.endTime) : ''}</div>
            <div class="event-actions">
                <button class="edit-btn" data-date="${date}" data-index="${index}">Edit</button>
                <button class="delete-btn" data-date="${date}" data-index="${index}">Delete</button>
            </div>
        `;
        details.style.display = 'block';

        // Add event listeners
        details.querySelector('.edit-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            editEvent(date, index);
        });
        details.querySelector('.delete-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            deleteEvent(date, index);
        });
    }
}

function createAddEventForm(date) {
    const form = document.createElement('form');
    form.className = 'add-event-form-inline';
    form.dataset.eventDate = date;

    form.innerHTML = `
        <div class="form-divider">Add New Event</div>
        <input type="text" name="title" class="event-input" placeholder="Event title" required>
        <textarea name="description" class="event-input" placeholder="Description (optional)" rows="2"></textarea>
        <div class="event-time-inputs">
            <input type="time" name="startTime" class="event-input" placeholder="Start time">
            <input type="time" name="endTime" class="event-input" placeholder="End time">
        </div>
        <button type="submit" class="event-button add-event-btn">Add Event</button>
    `;

    form.addEventListener('submit', (e) => handleFormSubmit(e, date));

    return form;
}

function handleFormSubmit(e, date) {
    e.preventDefault();

    const form = e.target;
    const title = form.querySelector('[name="title"]').value.trim();
    const description = form.querySelector('[name="description"]').value.trim();
    const startTime = form.querySelector('[name="startTime"]').value;
    const endTime = form.querySelector('[name="endTime"]').value;

    // Validate title
    if (!title) {
        alert('Please enter an event title');
        return;
    }

    // Validate time
    if (startTime && endTime && startTime > endTime) {
        alert('End time must be after start time');
        return;
    }

    const event = {
        title: title,
        description: description,
        date: date,
        startTime: startTime,
        endTime: endTime,
        timestamp: new Date().toISOString()
    };

    const events = getEventsForDate(date);
    events.push(event);
    localStorage.setItem(`events_${date}`, JSON.stringify(events));

    // Re-render the dialog
    const modal = document.querySelector('.calendar-modal');
    if (modal) {
        modal.remove();
    }
    showEventsForDate(date);

    // Refresh calendar to show has-events indicator
    refreshCalendar();
}

function showInlineModal(title, message, contentElement) {
    // Remove existing modal if present
    const existingModal = document.querySelector('.calendar-modal');
    if (existingModal) {
        existingModal.remove();
    }

    const modal = document.createElement('div');
    modal.className = 'calendar-modal';

    const modalContent = document.createElement('div');
    modalContent.className = 'calendar-modal-content';

    const modalTitle = document.createElement('h3');
    modalTitle.textContent = title;

    const modalMessage = document.createElement('p');
    modalMessage.textContent = message;

    modalContent.appendChild(modalTitle);
    if (message) modalContent.appendChild(modalMessage);
    if (contentElement) modalContent.appendChild(contentElement);

    const closeBtn = document.createElement('button');
    closeBtn.className = 'calendar-modal-close';
    closeBtn.innerHTML = '&times;';
    closeBtn.setAttribute('aria-label', 'Close');

    modalContent.appendChild(closeBtn);
    modal.appendChild(modalContent);

    document.body.appendChild(modal);

    // Close on click outside
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });

    closeBtn.addEventListener('click', function() {
        modal.remove();
    });

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const currentModal = document.querySelector('.calendar-modal');
            if (currentModal) {
                currentModal.remove();
            }
        }
    });

    return modal;
}

function formatDateDisplay(dateStr) {
    const [year, month, day] = dateStr.split('-').map(Number);
    const date = new Date(year, month - 1, day);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('ko-KR', options);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatTime(timeStr) {
    if (!timeStr || timeStr === '00:00') return '';
    return timeStr;
}

function refreshCalendar() {
    // Re-render calendar without page reload
    if (calendarContainer) {
        // Clear existing calendar
        calendarContainer.innerHTML = '';
        // Re-initialize
        initCalendar();
    }
}

function editEvent(date, index) {
    const events = getEventsForDate(date);
    if (!events || !events[index]) return;

    const event = events[index];

    // Close current modal
    const existingModal = document.querySelector('.calendar-modal');
    if (existingModal) existingModal.remove();

    // Create edit form
    const editContainer = document.createElement('div');
    editContainer.className = 'edit-event-form';

    editContainer.innerHTML = `
        <div class="form-divider">Edit Event</div>
        <input type="text" id="edit-title" class="event-input" value="${escapeHtml(event.title)}" required>
        <textarea id="edit-description" class="event-input" rows="2">${escapeHtml(event.description || '')}</textarea>
        <div class="event-time-inputs">
            <input type="time" id="edit-start-time" class="event-input" value="${event.startTime || ''}">
            <input type="time" id="edit-end-time" class="event-input" value="${event.endTime || ''}">
        </div>
        <button type="button" class="event-button update-event-btn">Update Event</button>
    `;

    // Show modal with edit form
    const editModal = showInlineModal('Edit Event', '', editContainer);

    // Add event listener for update button
    setTimeout(() => {
        const updateBtn = editContainer.querySelector('.update-event-btn');
        updateBtn.addEventListener('click', () => {
            const newTitle = document.getElementById('edit-title').value.trim();
            const newDescription = document.getElementById('edit-description').value.trim();
            const newStartTime = document.getElementById('edit-start-time').value;
            const newEndTime = document.getElementById('edit-end-time').value;

            if (!newTitle) {
                alert('Please enter an event title');
                return;
            }

            if (newStartTime && newEndTime && newStartTime > newEndTime) {
                alert('End time must be after start time');
                return;
            }

            events[index] = {
                title: newTitle,
                description: newDescription,
                date: date,
                startTime: newStartTime,
                endTime: newEndTime,
                timestamp: event.timestamp
            };

            localStorage.setItem(`events_${date}`, JSON.stringify(events));
            refreshCalendar();
            editModal.remove();
        });
    }, 0);
}

function deleteEvent(date, index) {
    if (!confirm('Are you sure you want to delete this event?')) return;

    const events = getEventsForDate(date);
    if (events && events[index]) {
        events.splice(index, 1);
        localStorage.setItem(`events_${date}`, JSON.stringify(events));
        refreshCalendar();

        // Close modal
        const modal = document.querySelector('.calendar-modal');
        if (modal) modal.remove();
    }
}

