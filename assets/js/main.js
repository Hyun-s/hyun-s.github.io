// Enhanced JavaScript for Hyunsoo Han's Personal Website Calendar
// This handles calendar functionality with localStorage and enhanced UX

// Global calendar container reference
let calendarContainer = null;

function initCalendar() {
    if (!calendarContainer) {
        calendarContainer = document.querySelector('.calendar-container');
    }

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

function initializeCalendar() {
    const today = new Date();
    currentYear = today.getFullYear();
    currentMonth = today.getMonth();

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

    // Add event form
    addEventForm(calendarContainer);

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

function addEventForm(container) {
    const form = document.createElement('div');
    form.className = 'add-event-form';
    form.innerHTML = `
        <h3>Add Event</h3>
        <input type="text" id="event-input" class="event-input" placeholder="Event title" required>
        <textarea id="event-description" class="event-input" placeholder="Event description"></textarea>
        <div class="event-time-inputs">
            <input type="time" id="event-time" class="event-input" placeholder="Start time">
            <input type="time" id="event-end-time" class="event-input" placeholder="End time">
        </div>
        <button type="button" class="event-button" id="save-event-btn">Save Event</button>
    `;
    container.appendChild(form);

    // Attach event listener after form is added
    const saveBtn = document.getElementById('save-event-btn');
    if (saveBtn) {
        saveBtn.addEventListener('click', saveEvent);
    }

    // Initialize input event handlers
    initInputHandlers();
}

function saveEvent() {
    const eventInput = document.getElementById('event-input');
    const descriptionInput = document.getElementById('event-description');
    const timeInput = document.getElementById('event-time');
    const endTimeInput = document.getElementById('event-end-time');

    // Check if in edit mode
    const saveBtn = document.getElementById('save-event-btn');
    const isEdit = saveBtn && saveBtn.dataset.editDate;

    if (isEdit) {
        editEventInPlace(saveBtn.dataset.editDate, saveBtn.dataset.editIndex);
        return;
    }

    const dateInput = document.getElementById('event-date');
    const date = dateInput ? dateInput.value : getCurrentSelectedDate();

    if (!date || !eventInput.value.trim()) {
        alert('Please select a date and enter an event title');
        return;
    }

    // Validate time
    const startTime = timeInput ? timeInput.value : '';
    const endTime = endTimeInput ? endTimeInput.value : '';

    if (startTime && endTime && startTime > endTime) {
        alert('End time must be after start time');
        return;
    }

    const event = {
        title: eventInput.value.trim(),
        description: descriptionInput.value.trim(),
        date: date,
        startTime: startTime,
        endTime: endTime,
        timestamp: new Date().toISOString()
    };

    const events = getEventsForDate(date);
    events.push(event);

    localStorage.setItem(`events_${date}`, JSON.stringify(events));

    // Clear form
    eventInput.value = '';
    descriptionInput.value = '';
    if (timeInput) timeInput.value = '';
    if (endTimeInput) endTimeInput.value = '';

    // Refresh calendar
    refreshCalendar();

    alert('Event saved successfully!');
}

function editEventInPlace(date, index) {
    const eventInput = document.getElementById('event-input');
    const descriptionInput = document.getElementById('event-description');
    const timeInput = document.getElementById('event-time');
    const endTimeInput = document.getElementById('event-end-time');

    if (!date || index === undefined) return;

    const events = getEventsForDate(date);
    if (!events[index]) return;

    // Validate time
    const startTime = timeInput ? timeInput.value : '';
    const endTime = endTimeInput ? endTimeInput.value : '';

    if (startTime && endTime && startTime > endTime) {
        alert('End time must be after start time');
        return;
    }

    events[index] = {
        title: eventInput.value.trim(),
        description: descriptionInput.value.trim(),
        date: date,
        startTime: startTime,
        endTime: endTime,
        timestamp: events[index].timestamp
    };

    localStorage.setItem(`events_${date}`, JSON.stringify(events));

    // Clear form and reset button
    eventInput.value = '';
    descriptionInput.value = '';
    if (timeInput) timeInput.value = '';
    if (endTimeInput) endTimeInput.value = '';

    const saveBtn = document.getElementById('save-event-btn');
    if (saveBtn) {
        delete saveBtn.dataset.editDate;
        delete saveBtn.dataset.editIndex;
        saveBtn.textContent = 'Save Event';
    }

    // Refresh calendar
    refreshCalendar();

    alert('Event updated successfully!');
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
        showInlineModal('No Events', `No events for ${date}`, []);
        return;
    }

    const eventList = document.createElement('div');
    eventList.className = 'event-list';

    events.forEach((event, index) => {
        const eventItem = document.createElement('div');
        eventItem.className = 'event-item';
        eventItem.innerHTML = `
            <div class="event-title">${escapeHtml(event.title)}</div>
            ${event.description ? `<div class="event-description">${escapeHtml(event.description)}</div>` : ''}
            <div class="event-time">${formatTime(event.startTime)} ${event.endTime ? '- ' + formatTime(event.endTime) : ''}</div>
            <div class="event-actions">
                <button class="edit-btn" data-index="${index}">Edit</button>
                <button class="delete-btn" data-index="${index}">Delete</button>
            </div>
        `;
        eventList.appendChild(eventItem);
    });

    showInlineModal(`Events for ${date}`, '', eventList);

    // Add event listeners for edit/delete
    setTimeout(() => {
        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                editEvent(date, parseInt(this.dataset.index));
            });
        });
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                deleteEvent(date, parseInt(this.dataset.index));
            });
        });
    }, 0);
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
        if (e.key === 'Escape' && modal) {
            modal.remove();
        }
    });
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

    const titleInput = document.getElementById('event-input');
    const descInput = document.getElementById('event-description');
    const timeInput = document.getElementById('event-time');
    const endTimeInput = document.getElementById('event-end-time');

    if (titleInput) titleInput.value = event.title || '';
    if (descInput) descInput.value = event.description || '';
    if (timeInput) timeInput.value = event.startTime || '';
    if (endTimeInput) endTimeInput.value = event.endTime || '';

    // Update the save button to indicate edit mode
    const saveBtn = document.getElementById('save-event-btn');
    if (saveBtn) {
        saveBtn.dataset.editDate = date;
        saveBtn.dataset.editIndex = index;
        saveBtn.textContent = 'Update Event';
    }

    // Close modal
    const modal = document.querySelector('.calendar-modal');
    if (modal) modal.remove();
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

function getCurrentSelectedDate() {
    // In a real implementation, this would return the selected date
    // For now, we'll use today's date
    const today = new Date();
    return `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
}

function initInputHandlers() {
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