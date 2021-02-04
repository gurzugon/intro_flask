$(function() {
     $('form').on('submit', function(event) {
           $.post('/process',
                  {
                    mass : $('#mass').val(),
                    velocity : $('#velocity').val()
                   },
                    function(data) {
                    var s = "The value of the kinetic energy is" + data.result
                    $('#result').text(s);
                });
              event.preventDefault();
     });
});
