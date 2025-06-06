function initCalendar(id) {
    const calendar_div = $(id);
    const calendar = new FullCalendar.Calendar(calendar_div[0], {
        initialView: 'dayGridMonth',
        themeSystem: 'bootstrap5',
        height: '100%',
        aspectRatio: 1.25,
        weekends: false,
        dayCellClassNames: 'calendar-day',
        buttonText: {
            today: 'Today'
        },
        headerToolbar: {
            left: 'title',
            center: '',
            right: 'prev today next'
        },
        events: [],
        eventDidMount: function(info) {
            info.el.title = `${info.event.extendedProps.status}`;
        }
    });
    calendar.render();
    return calendar;
}