$(document).ready(function() {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    $('#uploadButton').click(function() {
        const fileInput = $('#file')[0];
        const file = fileInput.files[0];
        
        if (!file) {
            showNotification('Please select a file.', 'danger');
            return;
        }

        socket.emit('upload_file', {
            filename: file.name,
            size: file.size,
            type: file.type,
            data: file
        });

        $('#loader').show();
    });

    socket.on('upload_response', function(response) {
        $('#loader').hide();
        if (response.success) {
            showNotification('File successfully uploaded', 'success');
            refreshFileList();
        } else {
            showNotification('Error uploading file: ' + response.error, 'danger');
        }
    });

    function refreshFileList() {
        $.ajax({
            url: '/recent_files',
            type: 'GET',
            success: function(data) {
                $('#file-list').empty();
                data.forEach(function(file, index) {
                    var row = $('<tr>');
                    row.append($('<th scope="row">').text(index + 1));
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
