let cached_pending_details = {};
let selected_leave_id = null;
let isRefreshing = false;

$(document).ready(function(){
    $('#toggleTableView')[0].checked = false;
    $('#adminComments').val('');

    // Begin loading employees data
    getRequestedLeave();

    // Initialise elements
    calendar = initCalendar('#calendar', 'auto', true);
    initSearch(
        '#employee-search', 
        '#employee-records-body tr', 
        [
            {selector: '.employee-name'},
            {selector: '.employee-id'}
        ]
    );
    initTableToggle();
});

function softRefresh(){
    if (isRefreshing) return;
    isRefreshing = true;
    $('.refresh').addClass('refresh-disabled');

    selected_leave_id = null;
    $('#adminComments').val('');
    deSelectRecord($('.selected-record'));
    calendar.removeAllEvents();
    getRequestedLeave();

    // Allow refresh again after a short delay
    setTimeout(() => {
        isRefreshing = false;
        $('.refresh').removeClass('refresh-disabled');
    }, 3000);
}

$('.refresh').on('click', softRefresh);

function getRequestedLeave(){
    $.ajax({
        url: '/leave/get_leave/requested',
        type: 'GET',
        beforeSend: function(){
            showLoader();
        },
        success: function(resp){
            if (resp){
                if (resp.error){
                    noRequestedLeave();
                    return
                }
                formatted = [...new Set(resp.map(record => record.fk_employee_id))];
                loadEmployees(formatted, false, true);
                cachePendingDetails(formatted);
            }
        },
        error: function(xhr, status, error) {
            console.log("Error loading requested leave: " + error);
            alert("Failed to load employees requested leave. Please try again later.");
        }
    });
}
function noRequestedLeave(){
    hideLoader();
    flashMessage('There are no active leave requests at the moment.<br> If you are expecting a leave request please double check it was submitted by the employee.', 'warning', 9000);
    $('.no-requests').show();
    $('#employee-records-body').hide();
}

function cachePendingDetails(data){
    //Format and cache pending leave
    data.forEach(id => {
        $.ajax({
            url: `/leave/get_leave/${id}`,
            type: 'GET',
            success: function(resp){
                resp.forEach(request => {
                    if (request.status !== 'Pending') return;

                    if (!cached_pending_details[id]) cached_pending_details[id] = {};
                    if (!cached_pending_details[id][request.pk_leave_id]) cached_pending_details[id][request.pk_leave_id] = request;
                });
            },
            complete: function(){
                getRemainingLeave(id);
                getDefaultLeave(id);
            },
            error: function(xhr, status, error) {
                console.log(`Error loading leave data for id ${id} : ${error}`);
            }
        });
    })
}

function getRemainingLeave(id){
    $.ajax({
        url: `/leave/get_leave/remaining/${id}`,
        type: 'GET',
        success: function(resp){
            if (resp[0]){
                Object.values(cached_pending_details[id]).forEach(value => {
                    value['leave_remaining'] = resp[0].leave_remaining
                    value['sick_leave_remaining'] = resp[0].sick_leave_remaining
                });
            } else {
                console.error(`No remaining leave data for id ${id}`)
            }
        },
        error: function(xhr, status, error) {
            console.log(`Error loading leave data for id ${id} : ${error}`);
        }
    });
}
function getDefaultLeave(id){
    $.ajax({
        url: `/employees/get_employees/${id}`,
        type: 'GET',
        success: function(resp){
            if (resp[0]){
                Object.values(cached_pending_details[id]).forEach(value => {
                    value['default_leave_balance'] = resp[0].default_leave_balance
                    value['default_sick_leave_balance'] = resp[0].default_sick_leave_balance
                });
            } else {
                console.error(`No default leave data for id ${id}`)
            }
        },
        error: function(xhr, status, error) {
            console.log(`Error loading employee data for id ${id} : ${error}`);
        }
    });
}

function approveLeave(id, comment){
    $.ajax({
        url: `/leave/update_leave/approve/${id}`,
        type: 'PUT',
        data: JSON.stringify({comment: comment}),
        contentType: 'application/json',
        success: function(resp){
            if (resp && resp.data === 'success'){
                softRefresh();
                $('.modal.show').modal('hide');
                flashMessage('Leave Approval Successful.', 'success', 3000);
            }
        },
        error: function(xhr, status, error) {
            console.log(`Error approving leave for id ${id} : ${error}`);
        }
    });
}
function rejectLeave(id, comment){
    $.ajax({
        url: `/leave/update_leave/deny/${id}`,
        type: 'PUT',
        data: JSON.stringify({comment: comment}),
        contentType: 'application/json',
        success: function(resp){
            if (resp && resp.data === 'success'){
                softRefresh();
                $('.modal.show').modal('hide');
                flashMessage('Leave Rejection Successful.', 'success', 3000);
            }
        },
        error: function(xhr, status, error) {
            console.log(`Error rejecting leave for id ${id} : ${error}`);
        }
    });
}

// Handles click of calendar event by populating leave modal
function handleEditClick(data){
    const leave_id = data.extendedProps.pk_leave_id;
    const leave_data = cached_pending_details[selected_employee_id][leave_id];

    selected_leave_id = leave_id;

    const date_requested = new Date(leave_data.date_requested).toLocaleString();
    const date_from = data.start;
    const date_to = new Date(leave_data.end_date);

    const employee_comments = leave_data.comment_employee;

    const modal = $('#viewRequest');

    modal.find('#requestTitleID').text(`Leave ID: ${leave_data.pk_leave_id}`);
    modal.find('#requestTitleType').text(`Leave Type: ${leave_data.leave_type}`);

    modal.find('.date-info .date-requested').text(date_requested);
    modal.find('.date-info .date-from').text(date_from.toLocaleDateString());
    modal.find('.date-info .date-to').text(date_to.toLocaleDateString());

    modal.find('.date-info .days-difference').text((data.end - data.start) / (1000 * 60 * 60 * 24)) //Use different start and end dates to help with calculating days
    modal.find('.date-info .default-leave').text(leave_data.default_leave_balance);
    modal.find('.date-info .default-sick-leave').text(leave_data.default_sick_leave_balance);
    modal.find('.date-info .leave-taken').text(leave_data.default_leave_balance - leave_data.leave_remaining);
    modal.find('.date-info .sick-leave-taken').text(leave_data.default_sick_leave_balance - leave_data.sick_leave_remaining);

    modal.find('#employeeComments').val(employee_comments);

    modal.modal('toggle');
}
$('.card-body #tableView').on('click', '.Pending', function(){
    const leave_id = $(this).closest('tbody').data('leave-id');
    const event = calendar.getEvents().find(ev =>
        ev.extendedProps.pk_leave_id === leave_id
    );
    calendar.gotoDate(event.start);
    const eventEl = $(`[data-pk-leave-id="${leave_id}"]`).first();
    if (eventEl.length) {
        eventEl[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));
    }
})

function closeModal(e){
    //Helper function to close modal and set selected leave state
    const modal = $(e.target).closest('.modal')
    selected_leave_id = null;
    $(modal).modal('toggle');
}
$('#viewRequest .btn-close').on('click', closeModal);
$('#viewRequest .close-modal').on('click', closeModal);

//Event handler for approving leave request
$('#approveRequestConfirm').on('click', function(){
    const comment = $('#adminComments').val();
    approveLeave(selected_leave_id, comment);
});
//Event handler for rejecting leave request
$('#denyRequestConfirm').on('click', function(){
    const comment = $('#adminComments').val();
    rejectLeave(selected_leave_id, comment);
});