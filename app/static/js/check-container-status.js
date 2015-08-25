function containerStatusChecker(taskId) {
    'use strict';

     $.ajax({
        url: '/container-startup-status/' + taskId,
        type: 'get',
        dataType: 'json',
        statusCode: {
            200: function(res) {
                if (res.href) {
                    window.location.href = res.href;
                }
            },
            404: function() {
               window.location.href = '/container/404';
            }
        },
        error: function onError() {
            console.log('Something went wrong');
        }
    });
}
