let cron_state = ""

window.onload = function() {
    document.getElementById("id_cron_time").onkeyup = function(event) {
        let target_elem = document.getElementById("id_describe_cron");
        if (event.target.value !== cron_state) {
            cron_state = event.target.value
            refresh_cron_description(event.target.value, target_elem);
        }
        };
    }

let refresh_cron_description = function(cron_str, target_elem) {
    const request = new XMLHttpRequest();
    const url = '/describe_cron?cron_str=' + cron_str
    request.open('GET', url);
    request.addEventListener(
        'readystatechange',
        () => {
            if (request.readyState === 4 && request.status === 200) {
                target_elem.value = JSON.parse(
                    request.responseText
                )["cron_description"]
            };
        }
    );
    request.send();
    return
}