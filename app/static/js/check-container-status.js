function containerStatusChecker(taskId) {
    'use strict';

     $.ajax({
        url: '/container-startup-status/' + taskId,
        type: 'get',
        dataType: 'json',
        statusCode: {
            200: function(res) {
                if (res.href) {
                    setTimeout(function() {
                        window.location.href = res.href;
                    }, 2000);
                } else {
                    window.location.href = '/container/404';
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
