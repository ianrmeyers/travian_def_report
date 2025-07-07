function updateServerTime() {
    $.getJSON('/server-time/', function(data) {
        $('#server-time').text(data.server_time);
    });
}

$(document).ready(function() {
    updateServerTime();
    setInterval(updateServerTime, 1000);
});