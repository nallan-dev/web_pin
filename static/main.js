
let refresh_rows = function() {
    $.ajax({
      type: 'GET',
      url: '/?ajax=1',
      data: ''
    }).done(function(data) {
      $('.rows-container').html(data);
    }).fail(function() {
      console.log('ajax_fail');
    });
}

let relay_button_onclick = function (elem) {
    elem.preventDefault();
    let $form = $(this);
    let form_data = $form.serialize();
    $.ajax({
      type: $form.attr('method'),
      url: $form.attr('action'),
      data: form_data
    }).done(function() {
      refresh_rows();
    }).fail(function() {
      console.log('fail');
    });
};

refresh_rows();
setInterval(function(){
    refresh_rows() // this will run after every 3 seconds
}, 3000);