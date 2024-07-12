// scripts.js

// Function to handle file upload
$(document).ready(function() {
    $('#uploadForm').submit(function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        
        // Show loading animation
        $('#loader').show();
        
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            success: function(data) {
                // Hide loading animation
                $('#loader').hide();
                
                // Show success notification
                showNotification('File successfully uploaded', 'success');
                
                // Clear file input
                $('#file').val('');
                
                // Refresh file list
                refreshFileList();
            },
            error: function(xhr, status, error) {
                // Hide loading animation
                $('#loader').hide();
                
                // Show error notification
                showNotification('Error uploading file: ' + error, 'danger');
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });
    
    // Function to refresh file list
    function refreshFileList() {
        $.ajax({
            url: '/recent_files',
            type: 'GET',
            success: function(data) {
                // Clear existing table rows
                $('#file-list').empty();
                
                // Append new rows
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
    
    // Function to show notification
    function showNotification(message, type) {
        var notification = $('#notification');
        notification.text(message).removeClass().addClass('notification alert alert-' + type);
        
        // Slide down animation
        notification.slideDown().delay(3000).slideUp();
    }
    
    // Call refreshFileList on page load
    refreshFileList();
});
