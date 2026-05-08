import React, { useState, useEffect } from 'react';
import './Calendar.css';

const Calendar = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [events, setEvents] = useState([]);
  const [showEventForm, setShowEventForm] = useState(false);
  const [selectedDate, setSelectedDate] = useState(null);
  const [eventForm, setEventForm] = useState({
    title: '',
    time: '',
    description: '',
    date: ''
  });

  // Load events from localStorage on component mount
  useEffect(() => {
    const savedEvents = localStorage.getItem('calendarEvents');
    if (savedEvents) {
      setEvents(JSON.parse(savedEvents));
    }
  }, []);

  // Save events to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('calendarEvents', JSON.stringify(events));
  }, [events]);

  const getDaysInMonth = (date) => {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
  };

  const getFirstDayOfMonth = (date) => {
    return new Date(date.getFullYear(), date.getMonth(), 1).getDay();
  };

  const formatDate = (date) => {
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const navigateMonth = (direction) => {
    const newDate = new Date(currentDate);
    newDate.setMonth(currentDate.getMonth() + direction);
    setCurrentDate(newDate);
  };

  const handleDateClick = (day) => {
    const clickedDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day);
    setSelectedDate(clickedDate);
    setEventForm({
      ...eventForm,
      date: clickedDate.toISOString().split('T')[0]
    });
    setShowEventForm(true);
  };

  const handleEventSubmit = (e) => {
    e.preventDefault();
    if (eventForm.title && eventForm.date) {
      const newEvent = {
        id: Date.now(),
        ...eventForm
      };
      setEvents([...events, newEvent]);
      setEventForm({
        title: '',
        time: '',
        description: '',
        date: ''
      });
      setShowEventForm(false);
    }
  };

  const handleEventInputChange = (e) => {
    const { name, value } = e.target;
    setEventForm({
      ...eventForm,
      [name]: value
    });
  };

  const getEventsForDate = (date) => {
    const dateStr = date.toISOString().split('T')[0];
    return events.filter(event => event.date === dateStr);
  };

  const renderCalendarDays = () => {
    const daysInMonth = getDaysInMonth(currentDate);
    const firstDayOfMonth = getFirstDayOfMonth(currentDate);

    const days = [];

    // Empty cells for days before the first day of the month
    for (let i = 0; i < firstDayOfMonth; i++) {
      days.push(<td key={`empty-${i}`} className="empty-day"></td>);
    }

    // Days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      const dateObj = new Date(currentDate.getFullYear(), currentDate.getMonth(), day);
      const dayEvents = getEventsForDate(dateObj);

      days.push(
        <td key={day} className="calendar-day" onClick={() => handleDateClick(day)}>
          <div className="day-number">{day}</div>
          <div className="events-preview">
            {dayEvents.slice(0, 2).map(event => (
              <div key={event.id} className="event-preview">
                {event.time || 'All day'} - {event.title}
              </div>
            ))}
            {dayEvents.length > 2 && (
              <div className="event-preview more-events">
                +{dayEvents.length - 2} more
              </div>
            )}
          </div>
        </td>
      );
    }

    return days;
  };

  const closeEventForm = () => {
    setShowEventForm(false);
    setSelectedDate(null);
    setEventForm({
      title: '',
      time: '',
      description: '',
      date: ''
    });
  };

  return (
    <div className="calendar">
      <div className="calendar-header">
        <button onClick={() => navigateMonth(-1)} className="nav-button">&lt; Prev</button>
        <h2>{currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}</h2>
        <button onClick={() => navigateMonth(1)} className="nav-button">Next &gt;</button>
      </div>

      <div className="calendar-grid">
        <div className="weekdays">
          <div className="weekday">Sun</div>
          <div className="weekday">Mon</div>
          <div className="weekday">Tue</div>
          <div className="weekday">Wed</div>
          <div className="weekday">Thu</div>
          <div className="weekday">Fri</div>
          <div className="weekday">Sat</div>
        </div>

        <div className="calendar-body">
          {renderCalendarDays()}
        </div>
      </div>

      {/* Event Form Modal */}
      {showEventForm && (
        <div className="modal-overlay" onClick={closeEventForm}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Add New Event</h3>
            <form onSubmit={handleEventSubmit}>
              <div className="form-group">
                <label htmlFor="title">Event Title:</label>
                <input
                  type="text"
                  id="title"
                  name="title"
                  value={eventForm.title}
                  onChange={handleEventInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="date">Date:</label>
                <input
                  type="date"
                  id="date"
                  name="date"
                  value={eventForm.date}
                  onChange={handleEventInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="time">Time:</label>
                <input
                  type="time"
                  id="time"
                  name="time"
                  value={eventForm.time}
                  onChange={handleEventInputChange}
                />
              </div>

              <div className="form-group">
                <label htmlFor="description">Description:</label>
                <textarea
                  id="description"
                  name="description"
                  value={eventForm.description}
                  onChange={handleEventInputChange}
                  rows="3"
                />
              </div>

              <div className="form-actions">
                <button type="submit" className="btn-primary">Add Event</button>
                <button type="button" className="btn-secondary" onClick={closeEventForm}>Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="events-list">
        <h3>Upcoming Events</h3>
        <div className="events-container">
          {events.length === 0 ? (
            <p>No events scheduled yet.</p>
          ) : (
            [...events]
              .sort((a, b) => new Date(a.date) - new Date(b.date))
              .map(event => (
                <div key={event.id} className="event-item">
                  <div className="event-date">
                    <div className="event-date-day">{new Date(event.date).getDate()}</div>
                    <div className="event-date-month">{new Date(event.date).toLocaleDateString('en-US', { month: 'short' })}</div>
                  </div>
                  <div className="event-details">
                    <h4>{event.title}</h4>
                    <p>{event.time || 'All day'} • {formatDate(new Date(event.date))}</p>
                    {event.description && <p className="event-description">{event.description}</p>}
                  </div>
                </div>
              ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Calendar;