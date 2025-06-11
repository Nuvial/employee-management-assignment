$(document).ready(function(){
    // Ensure calendar view is default
    $('#toggleTableView')[0].checked = false;

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
