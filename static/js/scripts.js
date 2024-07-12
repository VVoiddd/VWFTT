$(document).ready(function() {
    $('#uploadForm').submit(function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        
        $('#loader').show();
        
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            success: function(data) {
                $('#loader').hide();
                showNotification('File successfully uploaded', 'success');
                $('#file').val('');
                refreshFileList();
            },
            error: function(xhr, status, error) {
                $('#loader').hide();
                showNotification('Error uploading file: ' + error, 'danger');
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });

    function refreshFileList() {
        $.ajax({
            url: '/recent_files',
            type: 'GET',
            success: function(data) {
                $('#file-list').empty();
                data.forEach(function(file) {
                    var row = $('<tr>');
                    row.append($('<td>').text(file.filename));
                    row.append($('<td>').text(file.uploaded_at));
                    row.append($('<td>').text(file.uploaded_by));
                    $('#file-list').append(row);
                });
            },
            error: function(xhr, status, error) {
                console.error('Error fetching recent files:', error);
            }
        });
    }

    function showNotification(message, type) {
        var notification = $('#notification');
        notification.text(message).removeClass().addClass('notification alert alert-' + type);
        notification.slideDown().delay(3000).slideUp();
    }

    refreshFileList();
});
