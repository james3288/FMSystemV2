//save function for repair order
function saveForm(items){
    const form          = document.getElementById('form-' + items.random_item_code_id);
    const inputElements = form.querySelectorAll('input[type="text"]');
    const dateElements  = form.querySelectorAll('input[type="date"]');
    const alertID       = document.getElementById('wowAlertID-' + items.random_item_code_id);
    const closeButton   = document.querySelector('button[data-bs-dismiss="modal"]');

    let Empty = false;

    // this loop is for checking the input value if empty or not
    for (let i = 0; i < inputElements.length; i++) {
        if (inputElements[i].value === '') {
            Empty = true;
            break;
        }
    }

    // this loop is for checking the date value if empty or not
    dateElements.forEach(function(element) {
        const inputValue = element.value;
        const date = new Date(inputValue);
        
        if (isNaN(date)) {
        // Invalid date
        //   console.log('Invalid date:', inputValue);
            Empty = true;
        } else {
        // Valid date
            Empty = false;
        }
    });

    // console.log(Empty)

    //this statement will filter if some inputvalues and date are empty!
    if (Empty) {
        // At least one input value is empty
        alertID.style.display = 'block';
        alertID.innerHTML = `<div>Please fill up the following fields! </div>`;
        
        setTimeout(function() {
            alertID.style.display = 'none';
        }, 3000);

    //this statement is for true it means no problem above code
    } else {
        // All input values are not empty

        const formData = new FormData(form);

        fetch('/repair/', {
            method: 'POST',
            headers: {
            'X-CSRFToken': getCSRFToken() // Include CSRF token for security (see step 3)
            },
            body: formData
        })
            .then(function(response) {
            // Process the response from the Django view if needed
            console.log(response);
            })
            .catch(function(error) {
            console.log('Error:', error);
            });
        
        // perform click event to dismiss the modal
        // const clickEvent = new Event('click');
        // closeButton.dispatchEvent(clickEvent);
        
        location.reload(true);
        
    }
}
//save function for repairoder turnover
function DateTurnoverSaveForm(param, option,rep_released_id){

    var formdataid       = 'form-' + param
    var alertID          = 'wowAlertID-' + param
    var btnSaveID        = ''

    const form2          = document.getElementById(formdataid);
    const inputElements2 = form2.querySelectorAll('input[type="text"]');
    const dateElements2  = form2.querySelectorAll('input[type="date"]');
    const alertID2       = document.getElementById(alertID);
    const closeButton2   = document.querySelector('button[data-bs-dismiss="modal"]');

    let Empty2 = false;

    for (let i = 0; i < inputElements2.length; i++) {
        if (inputElements2[i].value == '') {
            Empty2 = true;
            break;
        }
    }

    dateElements2.forEach(function(element) {
        const inputValue2 = element.value;
        const date2 = new Date(inputValue2);
        
        if (isNaN(date2)) {
        // Invalid date
        //   console.log('Invalid date:', inputValue);
            Empty2 = true;
        } else {
        // Valid date
            Empty2 = false;
        }
    });

    console.log(Empty2)

    if (Empty2) {
        // At least one input value is empty
        alertID2.style.display = 'block';
        alertID2.innerHTML = `<div>Please fill up the following fields! </div>`;
        
        setTimeout(function() {
            alertID2.style.display = 'none';
        }, 3000);

    } else {
        // All input values are not empty

        const formData2 = new FormData(form2)

        formData2.append('rep_released_id', rep_released_id)    
        formData2.append('repair_order_id', param)
        formData2.append('option',option)
        
        //console.log(formData2)

        // var urls = ''

        // if (option == 'save'){
        //     urls = '/repair_turnover/'
        // }else{
        //     urls = '/repair_turnover_update/' 
        // }
        
        //console.log(formData2)

        fetch('/repair_turnover/', {
            method: 'POST',
            headers: {
            'X-CSRFToken': getCSRFToken() // Include CSRF token for security (see step 3)
            },
            body: formData2,
        })
            .then(function(response) {
            // Process the response from the Django view if needed
            console.log(response);
            })
            .catch(function(error) {
            console.log('Error:', error);
            });
        
        // perform click event to dismiss the modal
        // const clickEvent2 = new Event('click');
        // closeButton2.dispatchEvent(clickEvent2);
            location.reload(true);
            Empty2 = false;
    }
}
function getCSRFToken() {
    const cookieName = 'csrftoken';
    const cookieValue = document.cookie
    
    .split('; ')
    .find((row) => row.startsWith(`${cookieName}=`))
    .split('=')[1];

    console.log(cookieValue);
    return cookieValue;
}
function myAlert(caption){
    result = `<div class="alert alert-warning alert-dismissible fade show" role="alert">
                 
                ${caption}

                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>`

    return result

}
