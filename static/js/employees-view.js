let calendar;
let selected_employee_id = null;
let employee_leave = {}; // Cache for employee leave records
let employee_leave_calendar_cache = {}; // Cache for calendar events

$(document).ready(function(){
    // Ensure calendar view is default
    $('#toggleTableView')[0].checked = false;

    // Begin loading employees data
    loadEmployees();

    // Initialise elements
    calendar = initCalendar('#calendar');
    initSearch();
    initTableToggle();
});

function initSearch(){
    $('#employee-search').on('input', function(){
        const search = $(this).val().toLowerCase();
        const employee_table = $('#employee-records-body tr');
        employee_table.each(function(index, record){
            const id = $(record).data('employee-id').toString();
            const name = $(record).find('.employee-name').text().toLowerCase();
            if ((id.includes(search)) || name.includes(search)){
                $(record).show();
            } else {
                $(record).hide();
            }
        });
    });
}
function initTableToggle() {
    // Add event listener to toggle between table and calendar view for leave records
    $('#toggleTableView').on('change', function() {
        $('#calendar').toggle();
        $('#tableView').toggle();

        calendar.render();
    });
}

function loadEmployees() {
    $.ajax({
        url: '/employees/get_employees',
        type: 'GET',
        success: function(resp){
            if (resp.length > 0) {
                populateEmployeesRecords(resp);
                loadEmployeeStats();
                loadEmployeeLeave();
            }
        },
        error: function(xhr, status, error) {
            console.log("Error loading employees: " + error);
            alert("Failed to load employees data. Please try again later.");
        }
    });
}
function loadEmployeeStats(){
    $.ajax({
        url: '/stats/get_stats',
        type: 'GET',
        success: function(resp){
            if (resp.length > 0) {
                populateEmployeesRecordsStats(resp, 'stats');
            }
        },
        error: function(xhr, status, error) {
            console.log("Error loading employees: " + error);
            alert("Failed to load employees stats. Please try again later.");
        }
    });
}
function loadEmployeeLeave() {
    $.ajax({
        url: '/leave/get_leave',
        type: 'GET',
        success: function(resp){
            if (resp.length > 0) {
                // Populate employee leave for quick access without multiple AJAX calls
                resp.forEach(leave_rercord => {
                    if (!employee_leave[leave_rercord.fk_employee_id]) {
                        employee_leave[leave_rercord.fk_employee_id] = [];
                    }
                    employee_leave[leave_rercord.fk_employee_id].push({
                        leave_type: leave_rercord.leave_type,
                        start_date: leave_rercord.start_date,
                        end_date: leave_rercord.end_date,
                        status: leave_rercord.status
                    });
                });

                // Cache calendar events for each employee
                Object.keys(employee_leave).forEach(employee_id => {
                    if (!employee_leave_calendar_cache[employee_id]) {
                        employee_leave_calendar_cache[employee_id] = employee_leave[employee_id].map(record => {
                            return {
                                title: record.leave_type,
                                start: record.start_date,
                                end: record.end_date,
                                className: [record.status, 'calendar-event'],
                                textColor: 'black',
                                extendedProps: {
                                    status: record.status
                                }
                            };
                        });
                    }
                })
            }
        },
        complete: function() {
            // Populate employee leave records in table view
            populateLeaveTable();
        },
        error: function(xhr, status, error) {
            console.log("Error loading employees: " + error);
            alert("Failed to load employees leave. Please try again later.");
        }
    });

    $.ajax({
        url: '/leave/get_leave/remaining',
        type: 'GET',
        success: function(resp){
            populateEmployeesRecordsStats(resp, 'leave');
        },
        error: function(xhr, status, error) {
            console.log("Error loading employees: " + error);
            alert("Failed to load employees leave remaining. Please try again later.");
        }
    })
}

function populateEmployeesRecords(data) {
    const table_body = $('#employee-records-body');
    const stats_body = $('#employee-stats-body');

    table_body.empty();
    stats_body.empty();

    table_html = '';
    stats_html = '';
    data.forEach(function(employee_record) {
        table_html += `
        <tr data-employee-id="${employee_record.pk_employee_id}">
            <td class="employee-id">${employee_record.pk_employee_id}</td>
            <td class="employee-name">${employee_record.first_name} ${employee_record.last_name}</td>
        </tr>      
        `

        stats_html += `
        <div class="row h-100" style="display: none;" data-employee-id="${employee_record.pk_employee_id}">
            <div class="col-4 left">
                <div class="first-name">
                    <span class="label">First Name:</span>
                    <span>${employee_record.first_name}</span> 
                </div>
                <div class="last-name">
                    <span class="label">Last Name:</span>
                    <span>${employee_record.last_name}</span>
                </div>
                <hr>
                <div class="position">
                    <span class="label">Position:</span>
                    <span>${employee_record.employee_position}</span>
                </div>
                <div class="employee-id">
                    <span class="label">Employee ID:</span>
                    <span>${employee_record.pk_employee_id}</span>
                </div>
            </div>
            <div class="col-4 center">
                <div class="leave-balance">
                    <span class="label">Default Leave Balance:</span>
                    <span>${employee_record.default_leave_balance} days</span>
                </div>
                <div class="leave-remaining placeholder-glow">
                    <span class="label">Leave Remaining:</span>
                    <span class="employee-leave-remaining placeholder"></span>
                </div>
                <div class="sick-leave">
                    <span class="label">Default Sick Leave:</span>
                    <span>${employee_record.default_sick_leave_balance} days</span>
                </div>
                <div class="sick-leave-remaining placeholder-glow">
                    <span class="label">Sick Leave Remaining:</span>
                    <span class="employee-sick-remaining placeholder"></span>
                </div>
            </div>
            <div class="col-4 right">
                <div class="attendance placeholder-glow">
                    <span class="label">Attendance:</span>
                    <span class="employee-attendance placeholder"></span>
                </div>
                <div class="productivity placeholder-glow">
                    <span class="label">Productivity:</span>
                    <span class="employee-productivity placeholder"></span>
                </div>
                <div class="performance placeholder-glow">
                    <span class="label">Performance (0-10):</span>
                    <span class="employee-performance placeholder"></span>
                </div>
                <hr>
                <div class="last-updated placeholder-glow">
                    <span class="label">Last Updated:</span>
                    <span class="employee-stats-recorded placeholder"></span>
                </div>
            </div>
        </div>
        `
    });
    table_body.html(table_html);
    stats_body.html(stats_html);
}

function populateLeaveTable() {
    const leave_table_body = $('#tableView');

    let html = '';
    Object.keys(employee_leave).forEach(employee_id => {
        const leave_records = employee_leave[employee_id];
        html += `
            <table class="table table-striped table-bordered" data-employee-id="${employee_id}" style="display: none;">
                <thead>
                    <tr>
                        <th>Leave Type</th>
                        <th>Start Date</th>
                        <th>End Date</th>
                        <th>Status</th>
                    </tr>
                </thead>
        `
        leave_records.forEach(record => {
            html += `
                <tbody>
                    <tr>
                        <td>${record.leave_type}</td>
                        <td>${new Date(record.start_date).toLocaleDateString()}</td>
                        <td>${new Date(record.end_date).toLocaleDateString()}</td>
                        <td class="${record.status}">${record.status}</td>
                    </tr>
                </tbody>
            `
        });
        html += '</table>';
    });
    
    leave_table_body.html(html);
}


function populateEmployeesRecordsStats(data, field) {
    const stats_body = $('#employee-stats-body');

    stats_body.children().each(function(index, record) {
        const employee_id = $(record).data('employee-id');
        const target_data = data.find(target => target.fk_employee_id === employee_id);
        if (field === 'leave'){
            if (target_data) {
                try {
                    $(record).find('.employee-leave-remaining').text(`${target_data.leave_remaining} days`).removeClass('placeholder');
                    $(record).find('.employee-sick-remaining').text(`${target_data.sick_leave_remaining} days`).removeClass('placeholder');
                } catch (e) {
                    if (e instanceof TypeError){
                        console.log(`Employee ID ${employee_id} does not have a valid sick leave.`);
                    } else {
                        console.error(e);
                    }
                }
            }
        } else if (field === 'stats'){
            try {
                $(record).find('.employee-attendance').text(`${target_data.attendance} %`).removeClass('placeholder');
                $(record).find('.employee-productivity').text(`${target_data.productivity} %`).removeClass('placeholder');
                $(record).find('.employee-performance').text(`${target_data.performance}`).removeClass('placeholder');
                $(record).find('.employee-stats-recorded').text(`${new Date(target_data.date_recorded).toLocaleString()}`).removeClass('placeholder');
            } catch (e) {
                if (e instanceof TypeError){
                    console.error(`Employee ID: ${employee_id} does not have a stats record.`);
                } else {
                    console.error(e);
                }
            }
        }
    });
}

function handleStatsPeek(element){
    // Handle stats peek on hover
    const employee_id = $(element).data('employee-id');
    const stats_div = $(`#employee-stats-body div[data-employee-id="${employee_id}"]`); //Target stats div for the hovered employee

    $('#employee-stats-body div.row').hide(); // Hide all stats divs
    stats_div.removeClass('active-stats');
    stats_div.addClass('hover-stats').show(); // Show the hovered employees stats div
}
function handleLeavePeek(element, calendar) {
    // Create new event source for calendar
    calendar.removeAllEvents(); // Clear existing events from calendar
    const employee_id = $(element).data('employee-id')
    const calendar_container_div = $('.card-body.calendar-container');
    const events = employee_leave_calendar_cache[employee_id] || [];

    if (events.length === 0) { // If employee has no leave records set calendar to idle state
        calendar_container_div.removeClass('hover-calendar active-calendar').addClass('idle-calendar');
        $('#tableView table').hide(); // Hide all tables
        return;
    }

    calendar.addEventSource(events);
    calendar_container_div.removeClass('idle-calendar active-calendar').addClass('hover-calendar');

    // Show table view for the selected employee
    $('#tableView table').hide(); // Hide all tables
    $(`#tableView table[data-employee-id="${employee_id}"]`).show(); // Show the table for the hovered employee
}
function focusEmployeeRecord(element, calendar) {
    // Show stats for the selected employee by reusing hover functionality
    handleStatsPeek(element);
    $('#employee-stats-body div.hover-stats').removeClass('hover-stats').addClass('active-stats');

    // Show calendar for selected employee by reusing hover functionality
    handleLeavePeek(element, calendar);
    if ($('.card-body.calendar-container').hasClass('hover-calendar')) { // Only activate if calendar has events
        $('.card-body.calendar-container').removeClass('hover-calendar').addClass('active-calendar');
    }
}

$('#employee-records-body').on('mouseover', 'tr', function() {
    if (selected_employee_id) return; // Prevent hover event if an employee is selected
    handleStatsPeek(this);
    handleLeavePeek(this, calendar);
});
$('#employee-records-body').on('mouseleave', 'tr', function() {
    if (selected_employee_id) return; // Prevent hover event if an employee is selected
    $('#employee-stats-body div.hover-stats').removeClass('hover-stats').hide();
    $('.card-body.calendar-container').removeClass('hover-calendar').addClass('idle-calendar');
    calendar.removeAllEvents();
});
$('#employee-records-body').on('click', 'tr', function() {
    const employee_id = $(this).data('employee-id');

    if (selected_employee_id === employee_id) { // Deselect if already selected
        $(this).removeClass('selected-record');
        selected_employee_id = null;
        handleStatsPeek(this);
        handleLeavePeek(this, calendar);
        return;
    }

    selected_employee_id = employee_id; // Store selected employee ID
    $(this).siblings().removeClass('selected-record'); // Remove selection from other records if any
    $(this).addClass('selected-record'); // Add selection to the clicked record

    focusEmployeeRecord(this, calendar); // Focus on the clicked employee record
});
