/* eslint-disable no-invalid-this */

/**
 * @description search functionality
 */
$(document).ready(function() {
  $('#search').on('keyup', function() {
    const value = $(this).val().toLowerCase();
    $('#tbl tr').filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});

$(document).on('change', function() {
  if (data.length > 0) {
    $('#confirm').prop('disabled', false);
  } else {
    $('#confirm').prop('disabled', true);
  }
});

/**
 * @description button clicked
 */
$(document).ready(function() {
  $('#confirm').on('click', function() {
    let str = 'Making the following changes: \n';
    for (let i = 0; i < data.length; i++) {
      // eslint-disable-next-line max-len
      str += `user ${data[i].user} from ${data[i].current} to ${data[i].role} \n`;
    }
    alert(str);
    const jsonData = JSON.stringify(data);
    postData(jsonData);
    location.reload();
  });
});


const data = [];

/**
 * @description get the ID of the user and new role for any changed dropdowns.
 * Display alert if new role is not equal to previous role and add to data that
 * will be sent to server.
 */
$(document).ready(function() {
  $('td').change(function() {
    const userID = $(this).closest('tr').find('td:first').text().trim();
    // eslint-disable-next-line max-len
    const newRole = $(this).closest('tr').find('#user-role :selected').text().trim();
    // eslint-disable-next-line max-len
    const currentRole = $(this).closest('tr').find('#current-role').text().trim();
    console.log(userID);
    console.log(newRole);

    // Check that role doesn't equal previous role and it's not empty
    if (newRole != '') {
      let exists = false;
      let count = 0;

      // iterate through all existing objects
      for (let i = 0; i < data.length; i++) {
        if (data[i].user == userID) {
          exists = true;
          count = i;
          break;
        }
      } if (!exists) {
        if (currentRole != newRole) {
          // push to array only if it doesn't exist
          data.push({'user': userID, 'current': currentRole, 'role': newRole});
        }
      } else {
        if (currentRole != newRole) {
          // if it exists then update the newRole and do not push
          data[count].role = newRole;
        } else {
          // if current is new role then remove from array
          data.splice(count, 1);
        }
      }
    }
  });
});

/**
 * Send stuff
 * @param {*} jsonString
 */
async function postData(jsonString) {
  await $.ajax({
    url: '/users/update',
    type: 'POST',
    data: jsonString,
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    async: true,
    success: function(data, status, jqXHR) {
      return true;
    },
    error: function(jqXHR, status) {
      event.preventDefault();
      return false;
    },
  });
}
