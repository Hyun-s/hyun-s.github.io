import React, { useState } from 'react';
import './Calendar.css';

const Calendar = () => {
  const [currentDate, setCurrentDate] = useState(new Date());

  // Sample events data (this would normally come from an API)
  const sampleEvents = [
    {
      id: 1,
      title: 'Research Meeting',
      date: '2026-05-15',
      time: '10:00 AM',
      description: 'Weekly research meeting with team'
    },
    {
      id: 2,
      title: 'Conference Call',
      date: '2026-05-18',
      time: '2:00 PM',
      description: 'Collaboration with international partners'
    },
    {
      id: 3,
      title: 'Paper Submission Deadline',
      date: '2026-05-25',
      time: '11:59 PM',
      description: 'Submit paper to NeurIPS conference'
    },
    {
      id: 4,
      title: 'Lab Workshop',
      date: '2026-06-02',
      time: '9:00 AM',
      description: 'Internal workshop on new compression techniques'
    }
  ];

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
      const dateStr = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
      const dayEvents = sampleEvents.filter(event => event.date === dateStr);

      days.push(
        <td key={day} className="calendar-day">
          <div className="day-number">{day}</div>
          <div className="events-preview">
            {dayEvents.slice(0, 2).map(event => (
              <div key={event.id} className="event-preview">
                {event.time} - {event.title}
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

      <div className="events-list">
        <h3>Upcoming Events</h3>
        <div className="events-container">
          {sampleEvents.map(event => (
            <div key={event.id} className="event-item">
              <div className="event-date">
                <div className="event-date-day">{new Date(event.date).getDate()}</div>
                <div className="event-date-month">{new Date(event.date).toLocaleDateString('en-US', { month: 'short' })}</div>
              </div>
              <div className="event-details">
                <h4>{event.title}</h4>
                <p>{event.time} • {formatDate(new Date(event.date))}</p>
                <p className="event-description">{event.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Calendar;