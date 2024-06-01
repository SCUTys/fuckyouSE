

var buttons = document.querySelectorAll('.btn-color-1')

buttons.forEach(function(button) {
    button.addEventListener('click', function() {
      if (this.classList.contains('btn-color-1')) {
        this.classList.remove('btn-color-1');
        this.classList.add('btn-color-2');
      } 
      else {
        this.classList.remove('btn-color-2');
        this.classList.add('btn-color-1');
      }
    });
  });