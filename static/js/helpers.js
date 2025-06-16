/**
 * Show spinner loader with whole screen backdrop.
 */
function showLoader(){
    $('#spinnerLoader').addClass('active');
}
/**
 * Hide spinner loader with whole screen backdrop.
 */
function hideLoader(){
    $('#spinnerLoader').removeClass('active');
}

/**
 * Dynamically displays a Bootstrap alert message at the top right of the page.
 * @param {string} message - The message to display.
 * @param {string} [type='success'] - Bootstrap alert type: 'success', 'danger', 'warning', 'info'.
 * @param {number} [timeout=4500] - How long to show the message (ms).
 */
function flashMessage(message, type='success', timeout=3000) {
    const alert = $(`
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `);
    $('#flash-container').append(alert);
    setTimeout(() => {
        alert.alert('close');
    }, timeout);
}

/**
 * Initialises a FullCalendar instance. Events have to be dynamically added (Not accepted in the function). 
 * 
 * @param {string} id ID of the container div for the FullCalendar.
 * @param {boolean} edit Whether or not to enable editing of events.
 * @returns {Object} The FullCalendar instance object.
 */
function initCalendar(id, edit=false) {
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

/**
 * Initialises a form control to be a search bar for specified attributes in a search container.
 * 
 * @param {string} form Selector for the search input element.
 * @param {string} search_container  Selector for the body containing the records to search.
 * @param {Object[]} attributes Array of objects specifying the selectors for the attributes to search within.
 * @param {string} attributes[].selector Selector for the attribute to include in the search. 
 */
function initSearch(form, search_container, attributes){
    $(form).on('input', function(){
        const search = $(this).val().toLowerCase().split(' ');
        const records = $(search_container);
        records.each(function(index, record){
            let record_text = '';
            attributes.forEach(attr => {
                const value = $(record).find(attr.selector).text().toLowerCase();
                record_text += ` ${value}`;
            });
            
            const matches = search.every(term => record_text.includes(term));

            if (matches) {
                $(record).show();
            } else {
                $(record).hide();
            }
        });
    });
}

/**
 * Compares two objects deeply to check if they are equal.
 * 
 * @param {Object} obj1 
 * @param {Object} obj2 
 * @returns 
 */
function deepEqual(obj1, obj2) {
    if (obj1 === obj2) return true;
    if (typeof obj1 !== 'object' || obj1 === null || typeof obj2 !== 'object' || obj2 === null) {
        return false;
    }

    const keys1 = Object.keys(obj1);
    const keys2 = Object.keys(obj2);

    if (keys1.length !== keys2.length) {
        return false;
    }
    for (let key of keys1) {
        if (!keys2.includes(key) || !deepEqual(obj1[key], obj2[key])) {
            return false;
        }
    }

    return true;
}

/**
 * Turns regular element text fields into input fields preserving the current class list and any
 * units.
 * 
 * @param {String} selector A jquery selector string for the text to convert.
 */
function createInputFields(selector, size='sm', copy_classes=false){
    const fields = $(selector).find('.editable');
    fields.each(function(index, field){
        const classes = copy_classes ? $(field).attr('class'): '';
        const first_class = $(field).attr('class').split(' ')[0];
        const [value, unit] = $(field).text().split(' ');

        let input = `
            <div class="input-group input-group-${size} mb-1 has-validation">
                <input name="${first_class}" class="bs form-control ${classes}" value="${value}">
        `
        if (unit){
            input += `<span class="bs input-group-text">${unit}</span>`
        }
        input += `
                <div class="invalid-feedback"></div>
            </div>
        `

        $(field).replaceWith(input);
    });
}
/**
 * Turns regular input fields into text fields preserving the current class list and any
 * units.
 * 
 * @param {String} selector A jquery selector string for the input field to convert.
 */
function revertInputFields(selector, copy_classes=false){
    const fields = $(selector);
    fields.each(function(index, field){
        const input = $(field).find('input');
        const input_group_text = $(field).find('.input-group-text');
        const classes = copy_classes ? $(input).attr('class').replace('bs ', '').replace('form-control ', ''): '';
        const [value, unit] = [input.val(), input_group_text.text()];

        let text = `
            <span class="${classes}">${value} ${unit}</span>
        `

        $(field).replaceWith(text);
    });
}


/**
 * Simple check to test length of a string
 * @param {String} str 
 * @param {int} min 
 * @param {int} max 
 * @returns {Boolean}
 */
function isValidLength(str, min, max){
    return (str.length > min) && (str.length < max)
}
/**
 * Simple check to test if a string is alpha numeric
 * @param {String} str 
 * @returns {Boolean}
 */
function isAlphaNumeric(str) {
    return /^[a-z0-9]+$/i.test(str);
}
/**
 * Simple check if a string contains only numbers (0-9)
 * @param {String} str 
 * @returns {Boolean}
 */
function isNumeric(str) {
    if (str === '') return false
    return Number(str) !== NaN;
}
/**
 * Simple check if a string contains only letters (a-z, A-Z)
 * @param {String} str 
 * @returns {Boolean}
 */
function isAlphabetic(str) {
    return /^[a-zA-Z\s]+$/.test(str);
}
/**
 * Simple check if an int is a valid number based on min max
 * @param {int} number
 * @param {int} min
 * @param {int} max
 * @returns {Boolean}
 */
function isValidNumber(number, min, max){
    if (number === '') return false;
    const num = Number(number);
    return (num > min) && (num < max)
}