
function slugify(text) {
    return text
      .trim() // Remove leading and trailing whitespace
      .replace(/\s+/g, '-') // Replace spaces with hyphens
      .toLowerCase(); // Convert to lowercase
  }

function formatDate(originalDate){  
    // Step 3: Construct the "YYYY-MM-DD" format
    var year = originalDate.getFullYear();
    var month = addLeadingZero(originalDate.getMonth() + 1) // Months are zero-based, so we add 1
    var day = addLeadingZero(originalDate.getDate())

    // Step 4: Combine the parts into the desired format
    var formattedDate = year + '-' + month + '-' + day

    return formattedDate

}

function formatDate2(inputDate) {
    const date = new Date(inputDate);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    
    return `${year}-${month}-${day}`;
}

function addLeadingZero(value) {
    return value < 10 ? '0' + value : value
}
