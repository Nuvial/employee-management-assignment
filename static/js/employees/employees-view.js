$(document).ready(function(){
    // Ensure calendar view is default
    $('#toggleTableView')[0].checked = false;
    $('#viewSelector').val('View All');

    // Begin loading employees data
    loadEmployees();

    // Initialise elements
    calendar = initCalendar('#calendar');
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

function call(url, area, text, averages=false){
    $.ajax({
        url: `/stats/${area}/${url}`,
        type: 'GET',
        beforeSend: function(){
            $('.averages-text .label').text('');
            $('.averages-text .value').text('');
        },
        success: function(resp){
            if (resp.length > 1){
                const id_list = resp.map(id => id.fk_employee_id);
                loadEmployees(id_list);

                if (averages){
                    let percentage = area === 'attendance' ? '%' : '';
                    $('.averages-text .label').text(`${text} ${area}:`);
                    $('.averages-text .value').text(`${resp[0][`${text}_${area}`].toFixed(2)} ${percentage}`);
                }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
            }
        },
        complete: function(){
            hideLoader()
        },
        error: function(xhr, status, error) {
            console.error(`Could not get ${text} attendance: ${error}`);
            alert(`Failed to get ${text} attendance. Please try again later.`);
        }
    });
}

$('#viewSelector').on('change', function(){
    const option = $(this).val();
    showLoader();
    if (selected_employee_id){
        deSelectRecord($('.selected-record'));
    }

    if (option === 'View All'){
        $('.averages-text .label').text('');
        $('.averages-text .value').text('');
        loadEmployees();
    } else if (option === 'attendance-top5'){
        call('top5', 'attendance', 'top 5');
    } else if (option === 'attendance-bottom5'){
        call('bottom5', 'attendance', 'bottom 5');
    } else if (option === 'attendance-mean'){
        call('mean', 'attendance', 'mean', true);
    } else if (option === 'attendance-median'){
        call('median', 'attendance', 'median', true);
    } else if (option === 'attendance-range'){
        call('range', 'attendance', 'range', true);
    } else if (option === 'attendance-modal'){
        call('modal', 'attendance', 'modal', true);
    } else if (option === 'performance-top5'){
        call('top5', 'performance', 'top5');
    } else if (option === 'performance-bottom5'){
        call('bottom5', 'performance', 'bottom 5');
    } else if (option === 'performance-mean'){
        call('mean', 'performance', 'mean', true);
    } else if (option === 'performance-median'){
        call('median', 'performance', 'median', true);
    } else if (option === 'performance-range'){
        call('range', 'performance', 'range', true);
    } else if (option === 'performance-modal'){
        call('modal', 'performance', 'modal', true);
    }
});
